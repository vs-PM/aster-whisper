from pydantic_settings import BaseSettings
from pydantic import AnyUrl, validator, Field
from urllib.parse import quote

class AppSettings(BaseSettings):
    # Обязательные переменные
    ARI_USER: str = Field(..., description="ARI username")
    ARI_PASSWORD: str = Field(..., description="ARI password")
    ARI_APP: str = Field(..., description="Имя ARI приложения")
    ARI_MEDIA_HOST: str = Field(..., description="Хост для медиапотока")
    ARI_PORT: int = Field(2088, description="Порт для WebSocket ARI")
    ARI_MEDIA_PORT: int = Field(4000, description="Порт для raw-аудио")
    # VOSK_MODEL_PATH: str | None = Field(None, description="Путь к модели Vosk")
    
    # Динамически формируемая переменная
    ARI_WS_URL: AnyUrl | None = None

    @validator("ARI_WS_URL", pre=True, always=True)
    def assemble_ws_url(cls, v, values):
        if v:
            return v
        
        required = ["ARI_MEDIA_HOST", "ARI_PORT"]
        if any(field not in values for field in required):
            missing = [f for f in required if f not in values]
            raise ValueError(f"Не хватает переменных для формирования: {missing}")

        # encoded_user = quote(values["ARI_USER"], safe="")
        # encoded_password = quote(values["ARI_PASSWORD"], safe="")
        # encoded_app = quote(values["ARI_APP"], safe="")

        return f"ws://{values['ARI_MEDIA_HOST']}:{values['ARI_PORT']}/ari"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore" 

app_settings = AppSettings()
