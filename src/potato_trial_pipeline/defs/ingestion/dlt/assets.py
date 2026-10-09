import re

import dagster as dg
from dagster_dlt import DagsterDltResource, dlt_assets
import pandas as pd
import dlt
from pydantic import ValidationError
from pathlib import Path
from .trial import RejectedTrial, Trial
from ..utils.config import load_config
from ..utils.files import archive_file

SYMBOL_MAP = {
    ">=": "gte ",
    "<=": "lte ",
    ">": "gt ",
    "<": "lt ",
    "%": "percent ",
    "#": "hash ",
}


def clean_column_name(name: str) -> str:
    c = str(name).strip().lower()
    c = re.sub(r"\s+", " ", c)

    for symbol, text in SYMBOL_MAP.items():
        c = c.replace(symbol, text)

    c = re.sub(r"[^a-z0-9]+", "_", c)
    c = c.strip("_")

    if not c:
        return "val"
    if not c[0].isalpha():
        return f"val_{c}"

    return c


def _format_errors(exc: ValidationError) -> str:
    return " | ".join(
        f'{".".join(str(x) for x in err["loc"])}: {err["msg"]}, ({err.get("input")!r})'
        for err in exc.errors()
    )


@dlt.resource(name="excel_data", write_disposition="skip")
def load_data(file_path: str, sheet_name=0):
    file = Path(file_path)
    df = pd.read_excel(file, sheet_name=sheet_name)
    columns = [col for col in load_config().columns if col in df.columns]
    df = df[columns]
    data = df.to_dict(orient="records")

    for idx, row in enumerate(data, start=2):
        row = {clean_column_name(k): v for k, v in row.items()}
        row["source_file"] = file.name
        row["source_row"] = idx
        print(row)

        try:
            trial = Trial(**row).model_dump()
            yield {"ok": True, "data": trial}
        except ValidationError as err:
            row["error_message"] = _format_errors(err)
            yield {"ok": False, "data": row}


@dlt.transformer(
    name="trials",
    write_disposition="merge",
    primary_key=["year", "location", "experiment_name", "name1", "plot"],
    schema_contract={"tables": "evolve", "columns": "freeze", "data_type": "freeze"},
    columns=Trial,
)
def ingest_valid_rows(item: dict):
    if item["ok"]:
        yield item["data"]


@dlt.transformer(name="rejects", write_disposition="append", columns=RejectedTrial)
def ingest_quarantine_rows(item):
    if not item["ok"]:
        yield item["data"]


@dlt.source(name="potato_trial")
def trial_data_source(file_path: str):
    data_source = load_data(file_path)
    return [data_source | ingest_valid_rows, data_source | ingest_quarantine_rows]


trial_pipeline = dlt.pipeline(
    pipeline_name="dlt_trial_ingestion",
    destination=dlt.destinations.duckdb(credentials=load_config().paths.duckdb),
    dataset_name="met",
)


@dlt_assets(
    dlt_source=trial_data_source(file_path="__placeholder__"),
    group_name="trial_data",
    dlt_pipeline=trial_pipeline,
)
def trials(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    path = context.run_tags.get("file")

    if path is None:
        raise dg.Failure(f"File path missing")

    file = Path(path)

    if not file.exists():
        raise dg.Failure(f"File not found: {file}")

    context.log.info(f"Loading file: {file.name}")
    trial_pipeline.drop_pending_packages()
    yield from dlt.run(context=context, dlt_source=trial_data_source(str(file)))

    archive_file(Path(load_config().paths.archive), file)
    context.log.info(f"Archieved file: {file.name}")
