
# --- DEBUG LOGGING SETUP (для отладки, можно убрать в проде) ---
import logging
logging.basicConfig(
    level=logging.DEBUG,  # Для подробной отладки, можно сменить на INFO
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
# --- END DEBUG LOGGING SETUP ---

import wave
import json
from vosk import Model, KaldiRecognizer


logger = logging.getLogger("whisper_service")





import os

class WhisperTranscriber:
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = os.getenv("VOSK_MODEL_PATH", "model/vosk-model-ru-0.22")
        logger.info(f"Загрузка модели Vosk из '{model_path}'...")
        self.model = Model(model_path)
        logger.info("Vosk модель загружена")

    def transcribe(self, audio_path):
        """
        Транскрибирует WAV-файл в текст через Vosk.
        """
        logger.info(f"Начало транскрипции файла: {audio_path}")
        wf = None
        try:
            logger.info(f"Пытаюсь открыть файл: {audio_path}")
            wf = wave.open(audio_path, "rb")
            logger.info(f"Файл успешно открыт. Каналы: {wf.getnchannels()}, sample width: {wf.getsampwidth()}, framerate: {wf.getframerate()}")
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000, 44100]:
                logger.error(f"Неверный формат файла: каналы={wf.getnchannels()}, sample width={wf.getsampwidth()}, framerate={wf.getframerate()}")
                raise ValueError("Аудио должно быть WAV 16-bit mono, 8/16/44kHz")
            rec = KaldiRecognizer(self.model, wf.getframerate())
            text = ""
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    logger.info("Достигнут конец файла")
                    break
                if rec.AcceptWaveform(data):
                    res = rec.Result()
                    logger.debug(f"Partial result: {res}")
                    text += json.loads(res).get("text", "") + " "
            final_res = rec.FinalResult()
            logger.debug(f"Final result: {final_res}")
            text += json.loads(final_res).get("text", "")
            logger.info(f"Транскрипция завершена. Результат: {text.strip()}")
            return text.strip()
        except Exception as e:
            logger.error(f"Ошибка транскрипции через Vosk: {e}", exc_info=True)
            raise
        finally:
            if wf is not None:
                try:
                    wf.close()
                    logger.info(f"Файл {audio_path} закрыт.")
                except Exception as close_e:
                    logger.warning(f"Ошибка при закрытии файла: {close_e}")
