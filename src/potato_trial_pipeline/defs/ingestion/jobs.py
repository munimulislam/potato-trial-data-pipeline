import dagster as dg
from .assets import trials

file_ingest = dg.define_asset_job(
    name="trial_ingest", selection=[trials], tags={"duckdb": "trial"}
)
