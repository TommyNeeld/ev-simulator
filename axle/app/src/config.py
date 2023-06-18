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

    # version from version.env file
    class Config:
        env_file = "version.env"


settings = Settings()
