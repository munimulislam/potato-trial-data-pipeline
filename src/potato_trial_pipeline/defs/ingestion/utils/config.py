"""
@File - config.py
@Author - MdMunimul.Islam@teagasc.ie
@Created - 02/10/2026
@Description - Description of the file.
"""

import yaml
from pathlib import Path
from pydantic import BaseModel, ConfigDict
from functools import lru_cache


class PathConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    incoming: str
    archive: str
    duckdb: str


class ExcelConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    extensions: list[str]


class DataIngestConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    paths: PathConfig
    excel: ExcelConfig


@lru_cache
def load_config(
    config_path: str = str(Path(__file__).parent.parent / "pipeline.yaml"),
) -> DataIngestConfig:
    path = Path(config_path)
    config_dict = yaml.safe_load(path.read_text(encoding="utf-8"))

    return DataIngestConfig.model_validate(config_dict)
