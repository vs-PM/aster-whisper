from pydantic_settings import BaseSettings
import logging
from pathlib import Path

class Settings(BaseSettings):
    PROD: bool = False  # По умолчанию development режим

    @property
    def LOG_LEVEL(self) -> str:
        return "DEBUG" if not self.PROD else "INFO"

    @property
    def LOG_TO_FILE(self) -> bool:
        return self.PROD  # В продакшне логируем в файл

    @property
    def LOG_DIR(self) -> str:
        return "logs" if not self.PROD else "/var/log/app"  # Разные пути для dev/prod

    @property
    def log_level_int(self) -> int:
        return getattr(logging, self.LOG_LEVEL.upper(), logging.INFO)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()