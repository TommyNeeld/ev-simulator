"""
Load data from csv files
"""

import pandas as pd
from dateutil import parser
from config import settings
from functools import lru_cache


@lru_cache(maxsize=32)
def load_user_archetypes() -> pd.DataFrame:
    """Load user archetypes from csv file"""
    user_archetypes = pd.read_csv(settings.DATA_PATH.joinpath("user-archetypes.csv"))

    time_cols = ["ave_plug-in_time", "ave_plug-out_time"]
    for col in time_cols:
        user_archetypes[col] = user_archetypes[col].apply(
            lambda x: parser.parse(x).time()
        )

    perc_cols = ["ave_target_SoC", "ave_plug-in_SoC"]
    for col in perc_cols:
        user_archetypes[col] = user_archetypes[col].apply(
            lambda x: float(x.strip("%")) / 100
        )
    return user_archetypes


def load_archetypes_dash_table():
    """Load archetypes table for dash table."""
    df = load_user_archetypes()
    display_mapping = settings.USER_ARCHETYPES_DISPLAY_NAME_MAP
    columns = [
        {"name": display_mapping[col]["display_name"], "id": col}
        for col in df.columns
        if display_mapping[col]["show"]
    ]
    return df.to_dict("records"), columns
