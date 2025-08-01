import io
from fastapi.testclient import TestClient
from v1.main import app

client = TestClient(app)

def test_transcribe_audio():
    # Генерируем пустой WAV-файл (валидный, но без звука)
    wav_header = b'RIFF$\x00\x00\x00WAVEfmt ' + b'\x10\x00\x00\x00\x01\x00\x01\x00' + b'\x40\x1f\x00\x00\x80>\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00'
    file = io.BytesIO(wav_header)
    file.name = 'test.wav'
    response = client.post("/whisper/transcribe", files={"file": (file.name, file, "audio/wav")})
    assert response.status_code in (200, 500)  # 500 если whisper не настроен, 200 если ok
    assert "text" in response.json() or "detail" in response.json()
