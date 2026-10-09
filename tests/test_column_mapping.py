# tests/test_column_mapping.py
from pathlib import Path

import pandas as pd
import pytest

from potato_trial_pipeline.defs.ingestion.dlt.assets import (
    clean_column_name,
)
from potato_trial_pipeline.defs.ingestion.dlt.trial import Trial
from potato_trial_pipeline.defs.ingestion.utils.config import load_config

FIXTURES = Path(__file__).parent / "fixtures"
SAMPLE_FILES = sorted(FIXTURES.glob("*.xlsx*"))

MODEL_FIELDS = set(Trial.model_fields)
ADDED_BY_PIPELINE = {"source_file", "source_row"}


def cleaned_headers(path: Path) -> dict[str, str]:
    head = pd.read_excel(path, nrows=0)
    return {h: clean_column_name(h) for h in load_config().columns if h in head}


@pytest.mark.parametrize("path", SAMPLE_FILES, ids=lambda p: p.name)
def test_every_header_maps_to_a_trial_field(path):
    unmatched = {
        raw: clean
        for raw, clean in cleaned_headers(path).items()
        if clean not in MODEL_FIELDS
    }
    assert (
        not unmatched
    ), f"{path.name}: these headers match no Trial field:\n" + "\n".join(
        f"  {raw!r} -> {clean!r}" for raw, clean in unmatched.items()
    )


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("Experiment Name", "experiment_name"),
        (">=75 #", "gte_75_hash"),
        ("0-25 %", "val_0_25_percent"),
        ("Average length (mm) total", "average_length_mm_total"),
    ],
)
def test_exact_name(raw, expected):
    assert clean_column_name(raw) == expected
    assert expected in MODEL_FIELDS, f"{expected!r} is not a Trial field"
