from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import Optional

class DatabaseSettings(BaseSettings):
    POSTGRES_USER: str = Field(..., description="Имя пользователя PostgreSQL")
    POSTGRES_PASSWORD: str = Field(..., description="Пароль PostgreSQL")
    POSTGRES_DB: str = Field("postgres", description="Имя базы данных")
    POSTGRES_HOST: str = Field(..., description="Хост PostgreSQL")
    POSTGRES_PORT: str = Field("5432", description="Порт PostgreSQL")
    
    DATABASE_URL: Optional[str] = None

    @validator("DATABASE_URL", pre=True, always=True)
    def assemble_db_url(cls, v, values):
        if v:
            return v
        
        return (
            f"postgresql+asyncpg://{values['POSTGRES_USER']}:"
            f"{values['POSTGRES_PASSWORD']}@"
            f"{values['POSTGRES_HOST']}:"
            f"{values['POSTGRES_PORT']}/"
            f"{values['POSTGRES_DB']}"
        )

    class Config:
        env_file = ".env"
        env_prefix = "VOSK_"
        case_sensitive = False
        extra = "ignore"

db_settings = DatabaseSettings()
