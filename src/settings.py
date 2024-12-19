from pydantic import Field
from pydantic_settings import BaseSettings

from src.constants import ENV_PATH


class Settings(BaseSettings):
    """Базовые настройки для проекта."""

    app_name: str = Field(alias="APP_NAME", description="Имя приложения")
    database_url: str = Field(alias="DATABASE_URL", description="URL БД")
    exchange_api_key: str = Field(
        alias="API_KEY",
        description="Токен для апи валют."
    )
    exchange_api_url: str = Field(
        alias="EXCHANGE_API_URL", description="URL Путь до апи валют."
    )

    @property
    def exchange_api_url_latest(self) -> str:
        """Url для получения актуального курса валют."""
        return self.exchange_api_url + f"{self.exchange_api_key}/latest/"

    @property
    def exchange_api_url_pair(self) -> str:
        """Url для расчета обенного курса между валютами."""
        return self.exchange_api_url + f"/{self.exchange_api_key}/pair/"

    class Config:
        """Конфиг для settings."""

        env_file = ENV_PATH
        extra = "ignore"


settings = Settings()
