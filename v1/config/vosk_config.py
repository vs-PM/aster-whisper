from pydantic_settings import BaseSettings
from pydantic import Field, validator
from pathlib import Path
# from typing import Optional

class VoskSettings(BaseSettings):
    MODEL_PATH: Path = Field(..., description="Путь к модели Vosk")
    SAMPLE_RATE: int = Field(16000, description="Частота дискретизации аудио")
    RECOGNIZER_BUFFER: int = Field(4000, description="Размер буфера для распознавания")

    # @validator('MODEL_PATH', pre=True)
    # def validate_model_path(cls, value):
    #     if isinstance(value, str):
    #         return Path(value)
    #     return value

    # @validator('MODEL_PATH')
    # def check_model_exists(cls, value: Path):
    #     if not value.exists():
    #         raise ValueError(f"Vosk model not found at {value}")
    #     return value

    class Config:
        env_file = ".env"
        env_prefix = "VOSK_"
        case_sensitive = False
        extra = "ignore"

vosk_settings = VoskSettings()
