import json
import os
import wave
from typing import Optional

from dotenv import load_dotenv
from vosk import KaldiRecognizer, Model

load_dotenv()

class WhisperTranscriber:
    """
    Класс для транскрипции аудио через Vosk.
    """
    def __init__(self, model_path: Optional[str] = None) -> None:
        if model_path is None:
            model_path = os.getenv("VOSK_MODEL_PATH", "data/vosk-model-ru-0.42")
        self.model = Model(model_path)

    def transcribe(self, audio_path: str) -> str:
        """
        Транскрибирует WAV-файл в текст через Vosk.
        """
        wf = None
        try:
            wf = wave.open(audio_path, "rb")
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000, 44100]:
                raise ValueError("Аудио должно быть WAV 16-bit mono, 8/16/44kHz")
            rec = KaldiRecognizer(self.model, wf.getframerate())
            text = ""
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    res = rec.Result()
                    text += json.loads(res).get("text", "") + " "
            final_res = rec.FinalResult()
            text += json.loads(final_res).get("text", "")
            return text.strip()
        except Exception as e:
            raise
        finally:
            if wf is not None:
                wf.close()
