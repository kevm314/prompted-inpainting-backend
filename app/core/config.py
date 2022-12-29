import os
import secrets

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator
from typing import Any, Dict, List, Optional, Union

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "prompted-inpainting-prototype"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = eval(os.environ["CORS_DOMAINS"])

settings = Settings()