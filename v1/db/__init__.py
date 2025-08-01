# Пакет для работы с БД (инициализация подключения)
import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

Base = declarative_base()



VOSK_POSTGRES_USER = os.getenv("VOSK_POSTGRES_USER")
VOSK_POSTGRES_PASSWORD = os.getenv("VOSK_POSTGRES_PASSWORD")
VOSK_POSTGRES_DB = os.getenv("VOSK_POSTGRES_DB", "postgres")
VOSK_POSTGRES_HOST = os.getenv("VOSK_POSTGRES_HOST")
VOSK_POSTGRES_PORT = os.getenv("VOSK_POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql+asyncpg://{VOSK_POSTGRES_USER}:{VOSK_POSTGRES_PASSWORD}@{VOSK_POSTGRES_HOST}:{VOSK_POSTGRES_PORT}/{VOSK_POSTGRES_DB}"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
