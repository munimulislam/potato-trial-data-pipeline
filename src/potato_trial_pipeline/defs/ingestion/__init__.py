import dagster as dg
from .assets import trials
from .jobs import file_ingest
from .sensors import incoming_file_sensor
from .resources import dlt_resource


@dg.definitions
def definitions():
    return dg.Definitions(
        assets=[trials],
        jobs=[file_ingest],
        sensors=[incoming_file_sensor],
        resources={"dlt": dlt_resource},
    )
