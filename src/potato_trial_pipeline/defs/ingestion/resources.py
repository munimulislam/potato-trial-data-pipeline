import dagster as dg
from dagster_dlt import DagsterDltResource


@dg.resource
def dlt_resource():
    return DagsterDltResource()
