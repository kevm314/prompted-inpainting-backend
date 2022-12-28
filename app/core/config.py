import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "prompted-inpainting-prototype"
    # TODO: update with env variable
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['https://prod.d3ai0jorycnk11.amplifyapp.com']

settings = Settings()