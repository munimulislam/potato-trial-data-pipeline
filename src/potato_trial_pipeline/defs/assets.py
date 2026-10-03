"""
@File - assets.py
@Author - MdMunimul.Islam@teagasc.ie
@Created - 02/10/2026
@Description - Description of the file.
"""

from pathlib import Path

from dagster_dlt import DagsterDltResource, dlt_assets
import dagster as dg
from .ingestion.ingest import trial_pipeline, trial_data_source
from .ingestion.utils.files import discover_files, archive_file
from .ingestion.utils.config import load_config


class FileConfig(dg.Config):
    file_path: str


@dg.resource
def resources():
    return DagsterDltResource()


@dlt_assets(
    dlt_source=trial_data_source(file_path="__placeholder__"),
    dlt_pipeline=trial_pipeline,
    name="trial_ingestion",
)
def assets(
    context: dg.AssetExecutionContext,
    dlt: DagsterDltResource,
    config: FileConfig,
):
    path = Path(config.file_path)
    if not path.exists():
        raise dg.Failure(f"File not found: {path}")

    context.log.info(f"Loading file: {path.name}")
    yield from dlt.run(context=context, dlt_source=trial_data_source(str(path)))

    archive_file(Path(load_config().paths.archive), path)
    context.log.info(f"Archieved file: {path.name}")


ingest_job = dg.define_asset_job("file_ingest", selection=[assets])


@dg.sensor(
    job=ingest_job,
    minimum_interval_seconds=60,
    default_status=dg.DefaultSensorStatus.RUNNING,
)
def incoming_file_sensor(context):
    cfg = load_config()
    files = discover_files(cfg.paths.incoming, cfg.excel.extensions)

    if not files:
        yield dg.SkipReason("No file to process")
        return

    for f in files:
        yield dg.RunRequest(
            run_key=f"{f.name}:{f.stat().st_mtime_ns}",
            run_config=dg.RunConfig(
                ops={"trial_ingestion": FileConfig(file_path=str(f))}
            ),
        )
