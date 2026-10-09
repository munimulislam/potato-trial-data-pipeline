import dagster as dg
from .dlt.assets import trials
from .dlt.jobs import file_ingest
from .dlt.sensors import incoming_file_sensor
from .dlt.resources import dlt_resource


@dg.definitions
def definitions():
    return dg.Definitions(
        assets=[trials],
        jobs=[file_ingest],
        sensors=[incoming_file_sensor],
        resources={"dlt": dlt_resource},
    )
