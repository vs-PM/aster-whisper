import os
from v1.whisper.service import WhisperTranscriber

def test_vosk_transcribe():
    audio_path = os.path.join("tests", "whisper", "output.wav")
    transcriber = WhisperTranscriber()
    text = transcriber.transcribe(audio_path)
    print("Результат транскрипции:", text)

if __name__ == "__main__":
    test_vosk_transcribe()
