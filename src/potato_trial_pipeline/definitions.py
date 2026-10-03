"""
@File - definitions.py
@Author - MdMunimul.Islam@teagasc.ie
@Created - 02/10/2026
@Description - Description of the file.
"""

from pathlib import Path
from dagster import definitions, load_from_defs_folder


@definitions
def defs():
    return load_from_defs_folder(project_root=Path(__file__).parent.parent.parent)
