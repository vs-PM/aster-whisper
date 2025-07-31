import logging
from whisper import load_model


logger = logging.getLogger("whisper_service")


class WhisperTranscriber:
    def __init__(self, language='ru', model_size='small'):
        logger.info(f"Загрузка модели Whisper '{model_size}'...")
        self.model = load_model(model_size)
        self.language = language
        logger.info("Whisper модель загружена")

    def transcribe(self, audio_bytes):
        """
        Транскрибирует аудиофайл (WAV) в текст.
        Передаёт байты WAV напрямую в модель Whisper.
        """
        try:
            result = self.model.transcribe(audio_bytes, language=self.language)
            return result['text']
        except Exception as e:
            logger.error(f"Ошибка транскрипции через Whisper: {e}")
            raise
