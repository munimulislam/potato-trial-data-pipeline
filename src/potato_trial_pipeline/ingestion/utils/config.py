"""
@File - config.py
@Author - MdMunimul.Islam@teagasc.ie
@Created - 02/10/2026
@Description - Description of the file.
"""

import os

from dotenv import load_dotenv
import yaml
from pathlib import Path
from pydantic import BaseModel, ConfigDict, field_validator
from functools import lru_cache


def find_project_root(start: Path = Path(__file__).resolve()) -> Path:
    for folder in [start, *start.parents]:
        if (folder / "pyproject.toml").is_file():
            return folder
    raise FileNotFoundError(f"No pyproject.toml found above {start}")


PROJECT_ROOT = find_project_root()
load_dotenv(PROJECT_ROOT / ".env", override=False)


class PathConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    incoming: str
    archive: str
    duckdb: str

    @field_validator("incoming", "archive", mode="after")
    @classmethod
    def resolve_against_root(cls, value: Path) -> Path:
        return value if value.is_absolute() else (PROJECT_ROOT / value).resolve()


class IngestPipelineConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    paths: PathConfig
    file_extensions: list[str]
    columns: list[str]


@lru_cache
def load_config(config_file="pipeline.yaml") -> IngestPipelineConfig:
    config_path = PROJECT_ROOT / config_file
    if not config_path.is_file():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    config_dict = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    try:
        duckdb_path = os.environ["DUCKDB_PATH"]
    except KeyError:
        raise RuntimeError(
            "DUCKDB_PATH is not set. Add it to .env at the project root "
        )

    config_dict.setdefault("paths", {})["duckdb"] = duckdb_path

    config = IngestPipelineConfig.model_validate(config_dict)

    if not Path(config.paths.incoming).is_dir():
        raise FileNotFoundError(
            f"Incoming folder does not exist: {config.paths.incoming}"
        )

    if not Path(config.paths.duckdb).is_absolute():
        raise ValueError(
            f"DUCKDB_PATH must be an absolute path, got: {config.paths.duckdb}"
        )

    if not Path(config.paths.duckdb).parent.is_dir():
        raise FileNotFoundError(f"Folder for DuckDB file does not exist")

    Path(config.paths.archive).mkdir(parents=True, exist_ok=True)

    return IngestPipelineConfig.model_validate(config_dict)
