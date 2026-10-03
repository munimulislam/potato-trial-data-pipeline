"""
@File - standardise.py
@Author - MdMunimul.Islam@teagasc.ie
@Created - 02/10/2026
@Description - Description of the file.
"""

import pandas as pd
import re
from dataclasses import dataclass
from collections import Counter


@dataclass
class StandardisationResult:
    dataframe: pd.DataFrame
    column_rename_map: dict[str, str]


def clean_column_name(name: str) -> str:
    c = str(name).strip().lower()
    c = re.sub(r"\s+", " ", c)

    c = c.replace(">=", "gte")
    c = c.replace("<=", "lte")
    c = c.replace(">", "gt")
    c = c.replace("<", "lt")
    c = c.replace("%", "percent")
    c = c.replace("#", "hash")

    c = re.sub(r"[^a-z0-9]+", "_", c)
    c = re.sub(r"_+", "_", c).strip("_")

    if not c or not c[0].isalpha():
        c = f"col_{c}" if c else "col"

    return c


def get_duplicate_column_names(column_names: list[str]) -> list[str] | None:
    if len(column_names) != len(set(column_names)):
        duplicates = [c for c, n in Counter(column_names).items() if n > 1]
        return duplicates
    return None


def standardise_columns(df: pd.DataFrame) -> StandardisationResult:
    df = df.copy()
    original_col_names = list(df.columns)
    final_col_names = [clean_column_name(c) for c in df.columns]
    duplicate_columns = get_duplicate_column_names(final_col_names)

    if duplicate_columns:
        raise ValueError(
            f"Duplicate column names after standardisation: {duplicate_columns}"
        )

    df.columns = final_col_names

    rename_map = {
        str(original): str(final)
        for original, final in zip(original_col_names, final_col_names)
        if str(original) != str(final)
    }

    result = StandardisationResult(df, rename_map)

    return result
