from pathlib import Path

import dagster as dg
from dagster_dlt import DagsterDltResource, dlt_assets

from ...ingestion.pipeline import trial_data_source, trial_pipeline
from ...ingestion.utils.files import archive_file
from ...ingestion.utils.config import load_config


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
