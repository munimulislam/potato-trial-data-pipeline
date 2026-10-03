"""
@File - ingest.py
@Author - MdMunimul.Islam@teagasc.ie
@Created - 02/10/2026
@Description - Description of the file.
"""

import pandas as pd
import dlt
from pydantic import ValidationError
from pathlib import Path
from .standardise import standardise_columns
from .trial import Trial
from .utils.config import load_config


def _format_errors(exc: ValidationError) -> str:
    return " | ".join(
        f'{".".join(str(x) for x in err["loc"])}: {err["msg"]}, ({err.get("input")!r})'
        for err in exc.errors()
    )


@dlt.resource(name="excel_data", write_disposition="skip")
def load_data(file_path: str, sheet_name=0):
    file_name = Path(file_path).name
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    std_result = standardise_columns(df)
    df = std_result.dataframe

    for idx, row in enumerate(df.to_dict(orient="records"), start=2):
        row["source_file"] = file_name
        row["source_row"] = idx

        try:
            trial = Trial(**row).model_dump()
            yield {"ok": True, "data": trial}
        except ValidationError as err:
            row["error_message"] = _format_errors(err)
            yield {"ok": False, "data": row}


@dlt.transformer(
    name="trials",
    write_disposition={"disposition": "merge", "strategy": "scd2"},
    merge_key=["year", "location", "experiment_name", "name1", "plot"],
    schema_contract={"tables": "evolve", "columns": "evolve", "data_type": "freeze"},
)
def ingest_valid_rows(item: dict):
    if item["ok"]:
        yield item["data"]


@dlt.transformer(name="rejects", write_disposition="append")
def ingest_quarantine_rows(item):
    if not item["ok"]:
        yield item["data"]


@dlt.source(name="potato")
def trial_data_source(file_path: str):
    data_source = load_data(file_path)
    return [data_source | ingest_valid_rows, data_source | ingest_quarantine_rows]


trial_pipeline = dlt.pipeline(
    pipeline_name="dlt_trial_ingestion",
    destination=dlt.destinations.duckdb(credentials=load_config().paths.duckdb),
    dataset_name="trials",
)
