import logging
from faster_whisper import WhisperModel


logger = logging.getLogger("whisper_service")



class WhisperTranscriber:
    def __init__(self, language='ru', model_size='small'):
        logger.info(f"Загрузка модели FasterWhisper '{model_size}'...")
        self.model = WhisperModel(model_size, device="cpu")
        self.language = language
        logger.info("FasterWhisper модель загружена")

    def transcribe(self, audio_path):
        """
        Транскрибирует аудиофайл (WAV) в текст через FasterWhisper.
        Принимает путь к файлу.
        """
        try:
            segments, info = self.model.transcribe(audio_path, language=self.language)
            text = " ".join([segment.text for segment in segments])
            return text
        except Exception as e:
            logger.error(f"Ошибка транскрипции через FasterWhisper: {e}")
            raise
