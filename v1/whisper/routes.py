from fastapi import APIRouter, File, UploadFile, HTTPException
import logging
import tempfile
import os
from .service import WhisperTranscriber
from ..db.whisper_dao import WhisperTranscriptDAO


router = APIRouter(
    prefix="/whisper",
    tags=["Whisper"]
)
transcriber = WhisperTranscriber(language='ru', model_size='small')
logger = logging.getLogger("whisper_routes")


@router.get(
    "/ping",
    summary="Проверка whisper-сервиса",
    description="Проверка работоспособности whisper-сервиса."
)
def ping():
    return {"status": "whisper ok"}


@router.post(
    "/transcribe",
    summary="Транскрипция аудио (WAV)",
    description="Загрузка WAV-файла, транскрипция через Whisper, сохранение результата в БД."
)
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Эндпоинт для транскрипции аудиофайла (WAV) в текст.
    Сохраняет файл во временное хранилище, передаёт путь в Whisper, удаляет файл после обработки.
    Результат транскрипции сохраняется в БД (whisper_transcripts).
    """
    suffix = os.path.splitext(file.filename)[-1] or ".wav"
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            audio_path = tmp.name
        text = transcriber.transcribe(audio_path)
        await WhisperTranscriptDAO.create(file_name=file.filename, channel_id=None, text=text)
        return {"text": text}
    except Exception as e:
        logger.error(f"Ошибка транскрипции: {e}")
        raise HTTPException(status_code=500, detail="Ошибка транскрипции аудио")
    finally:
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.remove(audio_path)
