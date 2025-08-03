import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from .settings_logging import settings

def setup_logging() -> None:
    """Автоматическая настройка логгирования на основе режима PROD"""
    log_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    handlers = []
    
    # Консольный логгер всегда включен
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    handlers.append(console_handler)
    
    # Файловый логгер включается автоматически в PROD режиме
    if settings.LOG_TO_FILE:
        try:
            log_path = Path(settings.LOG_DIR)
            log_path.mkdir(parents=True, exist_ok=True)
            
            file_handler = RotatingFileHandler(
                log_path / "app.log",
                maxBytes=10*1024*1024,  # 10 MB
                backupCount=5 if settings.PROD else 2,
                encoding='utf-8'
            )
            file_handler.setFormatter(log_formatter)
            handlers.append(file_handler)
        except Exception as e:
            logging.error(f"Failed to setup file logging: {e}")

    # Настройка базового конфига
    logging.basicConfig(
        level=settings.log_level_int,
        handlers=handlers
    )
    
    # Дополнительные настройки для продакшна
    if settings.PROD:
        # Уменьшаем уровень логирования для внешних библиотек
        logging.getLogger('uvicorn').setLevel(logging.WARNING)
        logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
        logging.getLogger('uvicorn.error').setLevel(logging.WARNING)
        
        # Формат для файловых логов в prod может быть более подробным
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s'
        )
        for handler in handlers:
            if isinstance(handler, RotatingFileHandler):
                handler.setFormatter(file_formatter)
