import dagster as dg
import time
from ..utils.config import load_config
from ..utils.files import discover_files
from .jobs import file_ingest


@dg.sensor(
    job=file_ingest,
    minimum_interval_seconds=60,
    default_status=dg.DefaultSensorStatus.RUNNING,
)
def incoming_file_sensor(context):
    cfg = load_config()
    files = discover_files(cfg.paths.incoming, cfg.file_extensions)

    if not files:
        yield dg.SkipReason("No file to process")
        return

    for f in files:
        yield dg.RunRequest(
            run_key=f"{f.name}:{f.stat().st_mtime_ns}",
            tags={"file": str(f), "duckdb": "trial"},
        )
