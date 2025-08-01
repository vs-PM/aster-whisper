from pydantic_settings import BaseSettings

from dotenv import load_dotenv; load_dotenv()

class WhisperSettings(BaseSettings):
    WHISPER_MODEL: str = "small"
    WHISPER_LANGUAGE: str = "ru"

whisper_settings = WhisperSettings()
