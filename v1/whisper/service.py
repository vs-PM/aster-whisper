import json
import wave
from typing import Optional

from vosk import KaldiRecognizer
from v1.config.vosk_config import vosk_settings
from v1.vosk.model_manager import vosk_model


class WhisperTranscriber:
    """
    Класс для транскрипции аудио через Vosk.
    """
    def __init__(self, model_path: Optional[str] = None) -> None:
        # self.model = vosk_model.model
        self.sample_rate = vosk_settings.SAMPLE_RATE
        self.buffer_size = vosk_settings.RECOGNIZER_BUFFER

    def transcribe(self, audio_path: str) -> str:
        """
        Транскрибирует WAV-файл в текст через Vosk.
        Поддерживает форматы: 16-bit mono, 8/16/44.1 kHz
        """
        vosk_model.load_model()      # безопасно, если уже загружена - ничего не произойдет
        model = vosk_model.model
        wf = None
        try:
            wf = wave.open(audio_path, "rb")
            self._validate_audio_format(wf)

            rec = KaldiRecognizer(self.model, wf.getframerate())
            text_parts = []
            
            while True:
                data = wf.readframes(self.buffer_size)
                if not data:
                    break
                if rec.AcceptWaveform(data):
                    text_parts.append(json.loads(rec.Result())).get("text", "")

            text_parts.append(json.loads(rec.Result())).get("text", "")
            return " ".join(filter(None, text_parts)).strip()
        
        except Exception as e:
            raise RuntimeError(f"Audio transcription failed: {str(e)}")
        finally:
            if wf is not None:
                wf.close()

    def _validate_audio_format(self, wav_file):
        """Проверка формата аудиофайла"""
        if (wav_file.getnchannels() != 1 or 
            wav_file.getsampwidth() != 2 or 
            wav_file.getframerate() not in [8000, 16000, 44100]):
            raise ValueError(
                "Invalid audio format. Expected: WAV 16-bit mono, 8/16/44.1 kHz. "
                f"Got: {wav_file.getnchannels()} channels, "
                f"{wav_file.getsampwidth()*8}-bit, "
                f"{wav_file.getframerate()} Hz"
            )
