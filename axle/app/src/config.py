"""pydantic config class for the project"""

import pathlib
import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()

    # TODO: this should be a secret
    VALID_USERNAME_PASSWORD_PAIRS = {
        "tommy": "axleenergy1234",
    }

    # set VERSION to default value
    VERSION = "0.1.0"

    # dev or prod
    ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

    # TODO: this should be a secret
    SECRET_KEY = "SIUHfnw&WUH$"

    # css
    CUSTOM_CSS = "assets/custom.css"

    USER_ARCHETYPES_DISPLAY_NAME_MAP = {
        "name": {
            "display_name": "Archetype",
            "show": True,
        },
        "proportion": {
            "display_name": "Proportion",
            "show": True,
        },
        "ave_miles_per_yr": {
            "display_name": "Average Miles Per Year",
            "show": False,
        },
        "battery_ave_kWh": {
            "display_name": "Average Battery Size (kWh)",
            "show": True,
        },
        "ave_efficiency_mi_per_kWh": {
            "display_name": "Average Efficiency (mi/kWh)",
            "show": False,
        },
        "ave_plug-in_frequency_per_day": {
            "display_name": "Average Plug-in Frequency (per day)",
            "show": False,
        },
        "charger_kW": {
            "display_name": "Charger Power (kW)",
            "show": True,
        },
        "ave_plug-in_time": {
            "display_name": "Average Plug-in Time",
            "show": True,
        },
        "ave_plug-out_time": {
            "display_name": "Average Plug-out Time",
            "show": True,
        },
        "ave_target_SoC": {
            "display_name": "Average Target SoC",
            "show": False,
        },
        "ave_plug-in_SoC": {
            "display_name": "Average Plug-in SoC",
            "show": True,
        },
    }

    # version from version.env file
    class Config:
        env_file = "version.env"


settings = Settings()
