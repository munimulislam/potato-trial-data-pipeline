import re

import pandas as pd
from pydantic import AliasGenerator, BaseModel, Field, ConfigDict, model_validator


class Trial(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    experiment_name: str = Field(min_length=1)
    location: str = Field(min_length=1)
    name1: str = Field(min_length=1)
    plot: int = Field(gt=0)
    year: int
    source_file: str = Field(min_length=1)
    source_row: int = Field(gt=0)

    origin: str | None = Field(default=None)
    tubersize: float | None = Field(default=None)
    eveness: float | None = Field(default=None)
    appearance: float | None = Field(default=None)
    tubnumbers: float | None = Field(default=None)
    ffscab: float | None = Field(default=None)
    ffdefects: float | None = Field(default=None)
    ffhollowh: float | None = Field(default=None)
    ff_irs: float | None = Field(default=None)
    eyedepth: float | None = Field(default=None)
    o_a_score: float | None = Field(default=None)
    tubshape: str | None = Field(default=None)
    skincolour: str | None = Field(default=None)
    fleshcolou: str | None = Field(default=None)
    comments: str | None = Field(default=None)
    dryness: float | None = Field(default=None)
    drymatter: float | None = Field(default=None)
    finalyield: float | None = Field(default=None)
    uniformity: float | None = Field(default=None)
    dsntgrtn: float | None = Field(default=None)
    mealiness: float | None = Field(default=None)
    utilisatio: float | None = Field(default=None)
    acb: float | None = Field(default=None)
    ovall_cook: float | None = Field(default=None)
    crisp: float | None = Field(default=None)
    coflscol: float | None = Field(default=None)
    acb24: float | None = Field(default=None)
    flavour: float | None = Field(default=None)
    chipcolour: float | None = Field(default=None)
    hunterl: float | None = Field(default=None)
    huntera: float | None = Field(default=None)
    hunterb: float | None = Field(default=None)
    cook_com: str | None = Field(default=None)
    crisp_yr4: float | None = Field(default=None)
    crisp_3m8d: float | None = Field(default=None)
    crisp_3m4d: float | None = Field(default=None)
    chip_3m8d: float | None = Field(default=None)
    chip_3m4d: float | None = Field(default=None)
    huntl_3m8d: float | None = Field(default=None)
    hunta_3m8d: float | None = Field(default=None)
    huntb_3m8d: float | None = Field(default=None)
    huntl_3m4d: float | None = Field(default=None)
    hunta_3m4d: float | None = Field(default=None)
    huntb_3m4d: float | None = Field(default=None)
    chpcom3m8d: float | None = Field(default=None)
    chpcom3m4d: float | None = Field(default=None)
    ffrots: float | None = Field(default=None)
    crisp_6m8d: float | None = Field(default=None)
    crisp_6m4d: float | None = Field(default=None)
    chip_6m8d: float | None = Field(default=None)
    chip_6m4d: float | None = Field(default=None)
    chpcom6m8d: float | None = Field(default=None)
    chpcom6m4d: float | None = Field(default=None)
    huntl_6m8d: float | None = Field(default=None)
    huntl_6m4d: float | None = Field(default=None)
    hunta_6m8d: float | None = Field(default=None)
    hunta_6m4d: float | None = Field(default=None)
    huntb_6m8d: float | None = Field(default=None)
    huntb_6m4d: float | None = Field(default=None)
    average_length_mm_gte_55: float | None = Field(default=None)
    average_length_mm_gte_60: float | None = Field(default=None)
    average_length_mm_gte_65: float | None = Field(default=None)
    average_length_mm_gte_70: float | None = Field(default=None)
    average_length_mm_gte_75: float | None = Field(default=None)
    average_length_mm_0_25: float | None = Field(default=None)
    average_length_mm_25_28: float | None = Field(default=None)
    average_length_mm_28_35: float | None = Field(default=None)
    average_length_mm_35_40: float | None = Field(default=None)
    average_length_mm_40_45: float | None = Field(default=None)
    average_length_mm_45_50: float | None = Field(default=None)
    average_length_mm_50_55: float | None = Field(default=None)
    average_length_mm_55_60: float | None = Field(default=None)
    average_length_mm_60_65: float | None = Field(default=None)
    average_length_mm_65_70: float | None = Field(default=None)
    average_length_mm_70_75: float | None = Field(default=None)
    average_length_mm_total: float | None = Field(default=None)
    average_nir_value_total: float | None = Field(default=None)
    total_hash: float | None = Field(default=None)
    weight_percent_gte_75: float | None = Field(default=None)
    weight_percent_0_25: float | None = Field(default=None)
    weight_percent_25_28: float | None = Field(default=None)
    weight_percent_28_35: float | None = Field(default=None)
    weight_percent_35_40: float | None = Field(default=None)
    weight_percent_40_45: float | None = Field(default=None)
    weight_percent_45_50: float | None = Field(default=None)
    weight_percent_50_55: float | None = Field(default=None)
    weight_percent_55_60: float | None = Field(default=None)
    weight_percent_60_65: float | None = Field(default=None)
    weight_percent_65_70: float | None = Field(default=None)
    weight_percent_70_75: float | None = Field(default=None)
    weight_g_gte_75: float | None = Field(default=None)
    weight_g_0_25: float | None = Field(default=None)
    weight_g_25_28: float | None = Field(default=None)
    weight_g_28_35: float | None = Field(default=None)
    weight_g_35_40: float | None = Field(default=None)
    weight_g_40_45: float | None = Field(default=None)
    weight_g_45_50: float | None = Field(default=None)
    weight_g_50_55: float | None = Field(default=None)
    weight_g_55_60: float | None = Field(default=None)
    weight_g_60_65: float | None = Field(default=None)
    weight_g_65_70: float | None = Field(default=None)
    weight_g_70_75: float | None = Field(default=None)
    weight_g_total: float | None = Field(default=None)
    gte_75_hash: float | None = Field(default=None)
    gte_75_percent: float | None = Field(default=None)
    val_0_25_hash: float | None = Field(default=None)
    val_0_25_percent: float | None = Field(default=None)
    val_25_28_hash: float | None = Field(default=None)
    val_25_28_percent: float | None = Field(default=None)
    val_28_35_hash: float | None = Field(default=None)
    val_28_35_percent: float | None = Field(default=None)
    val_35_40_hash: float | None = Field(default=None)
    val_35_40_percent: float | None = Field(default=None)
    val_40_45_hash: float | None = Field(default=None)
    val_40_45_percent: float | None = Field(default=None)
    val_45_50_hash: float | None = Field(default=None)
    val_45_50_percent: float | None = Field(default=None)
    val_50_55_hash: float | None = Field(default=None)
    val_50_55_percent: float | None = Field(default=None)
    val_55_60_hash: float | None = Field(default=None)
    val_55_60_percent: float | None = Field(default=None)
    val_60_65_hash: float | None = Field(default=None)
    val_60_65_percent: float | None = Field(default=None)
    val_65_70_hash: float | None = Field(default=None)
    val_65_70_percent: float | None = Field(default=None)
    val_70_75_hash: float | None = Field(default=None)
    val_70_75_percent: float | None = Field(default=None)
    average_length_mm_gte_25: float | None = Field(default=None)
    average_length_mm_gte_28: float | None = Field(default=None)
    average_length_mm_gte_35: float | None = Field(default=None)
    average_length_mm_gte_40: float | None = Field(default=None)
    average_length_mm_gte_45: float | None = Field(default=None)
    average_length_mm_gte_50: float | None = Field(default=None)
    plot_size_lt: float | None = Field(default=None)
    yield_total_t_ha: float | None = Field(default=None)
    yield_gte_80_t_ha: float | None = Field(default=None)
    yield_0_35_t_ha: float | None = Field(default=None)

    @model_validator(mode="before")
    @classmethod
    def clean_all_nans(cls, data: dict) -> dict:
        if not isinstance(data, dict):
            return data

        cleaned = {}

        for key, val in data.items():
            if val is None or pd.isna(val):
                cleaned[key] = None
            elif isinstance(val, str):
                stripped = val.strip()
                if stripped == "":
                    cleaned[key] = None
                else:
                    try:
                        num = float(stripped)
                    except ValueError:
                        cleaned[key] = stripped
                    else:
                        cleaned[key] = None if num < 0 else stripped
            elif isinstance(val, bool):
                cleaned[key] = val
            elif isinstance(val, (int, float)) and val < 0:
                cleaned[key] = None
            elif isinstance(val, int) and key not in ["Year", "Plot"]:
                cleaned[key] = float(val)
            else:
                cleaned[key] = val
        return cleaned


class RejectedTrial(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    source_file: str = Field(min_length=1)
    source_row: int = Field(gt=0)
    error_message: str = Field(min_length=1)
