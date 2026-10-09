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


class IngestPipelineConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    paths: PathConfig
    file_extensions: list[str]
    columns: list[str]


@lru_cache
def load_config(config_path="pipeline.yaml") -> IngestPipelineConfig:
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"File pipeline.yaml not found in project root")

    config_dict = yaml.safe_load(path.read_text(encoding="utf-8"))

    return IngestPipelineConfig.model_validate(config_dict)
