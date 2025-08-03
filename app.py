import logging
import socket
from contextlib import asynccontextmanager
from urllib.parse import urlparse
from fastapi import FastAPI
from fastapi.logger import logger

from v1.ari.worker import _worker, check_ari_connection
from v1.docx.routes import router as docx_router
from v1.whisper.routes import router as whisper_router
from v1.config.logging_config import setup_logging
from v1.config.logging_config import settings
from v1.vosk.model_manager import vosk_model

# Настройка логгера
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Контекстный менеджер жизненного цикла приложения"""
    logger.info(f"Application starting in {'PRODUCTION' if settings.PROD else 'DEVELOPMENT'} mode")
    logger.debug(f"Logging configuration: "
                f"Level={settings.LOG_LEVEL}, "
                f"File logging={'ENABLED' if settings.LOG_TO_FILE else 'DISABLED'}, "
                f"Log dir={settings.LOG_DIR}")
    # Проверка подключения к Asterisk
    if await check_ari_connection():
        try:
            vosk_model.load_model()     # <-- ЗАГРУЗИТЬ МОДЕЛЬ ЯВНО!
            _worker.model = vosk_model.model
            _worker.start()
            logger.info("ARI worker успешно запущен")
        except Exception as e:
            logger.error(f"Ошибка при запуске ARI worker: {e}")
    else:
        logger.warning("ARI worker не запущен из-за проблем с подключением к Asterisk")
    
    yield
    logger.info("Приложение завершает работу")

def create_app() -> FastAPI:
    """Фабрика для создания экземпляра FastAPI приложения"""
    app = FastAPI(
        title="PM_work v1",
        description="API для работы с docx-документами и транскрипцией аудио через Whisper.",
        version="1.0.0",
        contact={
            "name": "PM_work API Support",
            "email": "log4v7@gmail.com"
        },
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )

    # Регистрация роутеров
    app.include_router(whisper_router, prefix="/api/v1")
    app.include_router(docx_router, prefix="/api/v1")

    @app.get("/")
    async def root():
        return {
            "message": "PM_work v1 API",
            "status": "running",
            "documentation": {
                "swagger": "/docs",
                "redoc": "/redoc"
            }
        }

    @app.get("/health")
    async def health_check():
        """Эндпоинт для проверки здоровья сервиса"""
        return {"status": "healthy"}
    
    return app

app = create_app()