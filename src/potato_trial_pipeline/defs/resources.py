"""
@File - resources.py
@Author - MdMunimul.Islam@teagasc.ie
@Created - 02/10/2026
@Description - Description of the file.
"""

import dagster as dg
from dagster_dlt import DagsterDltResource


@dg.definitions
def resources():
    return dg.Definitions(resources={"dlt": DagsterDltResource()})
