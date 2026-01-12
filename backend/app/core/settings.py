import functools
from pathlib import Path
from typing import Any, Self

import dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path.cwd() / ".env"
BASE_DIR = Path(__file__).resolve().parents[2]


class InjectableSettings(BaseSettings):
    @classmethod
    def new(cls) -> Self:
        return cls()


class AppSettings(InjectableSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix="APP_",
        extra="ignore",
    )

    DEBUG: bool = True
    DEVELOP: bool = True

    PROJECT_NAME: str = "app"
    VERSION: str = "0.0.1"
    ENVIRONMENT: str = "local"

    ALLOW_ORIGINS: list[str] = [
        "http://localhost:8000",
    ]
    ALLOW_ORIGIN_REGEX: str | None = r"https://(.*\.)?localhost\.com"

    FRONTEND_HOST: str = "http://localhost:5173"

    @staticmethod
    def get_develop_settings() -> dict[str, Any]:
        return {
            "host": "localhost",
            "port": 8000,
            "reload": True,
        }

    @staticmethod
    def get_prod_settings() -> dict[str, Any]:
        return {
            "host": "0.0.0.0",
            "port": 8001,
        }


class BaseClientSettings(InjectableSettings):
    BASE_URL: str
    TIMEOUT: int = 10

    @field_validator("BASE_URL")
    @classmethod
    def strip_trailing_slash(cls, v: str) -> str:
        return v.rstrip("/")


class IpWhoIsClientSettings(BaseClientSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix="API_IP_WHOIS_",
        extra="ignore",
    )

    BASE_URL: str = "http://ipwho.is/"


class IpInfoClientSettings(BaseClientSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix="API_IP_INFO_",
        extra="ignore",
    )

    BASE_URL: str = "https://ipinfo.io"


class CrtShClientSettings(BaseClientSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix="API_CRT_SH_",
        extra="ignore",
    )

    BASE_URL: str = "https://crt.sh"


class DatabaseSettings(InjectableSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix="DB_",
        extra="ignore",
    )

    DRIVER: str = "sqlite+aiosqlite"
    NAME: str = "db.sqlite3"

    ECHO: bool = False
    TIMEOUT: int = 5

    @property
    def url(self) -> str:
        return f"{self.DRIVER}:///{BASE_DIR}/{self.NAME}"


@functools.cache
def _load_dotenv_once() -> None:
    dotenv.load_dotenv()


def get_settings[TSettings: BaseSettings](cls: type[TSettings]) -> TSettings:
    _load_dotenv_once()
    return cls()
