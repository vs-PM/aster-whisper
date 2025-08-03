import logging
from pathlib import Path
import tempfile
from fastapi.responses import JSONResponse
from fastapi import APIRouter, File, HTTPException, UploadFile

from v1.db.whisper_dao import WhisperTranscriptDAO

from .service import WhisperTranscriber

router = APIRouter(
    prefix="/whisper",
    tags=["Whisper"]
)
transcriber = WhisperTranscriber()
logger = logging.getLogger("whisper_routes")


@router.get(
    "/ping",
    summary="Проверка whisper-сервиса",
    description="Проверка работоспособности whisper-сервиса."
)
def ping():
    return {"status": "service ok"}


@router.post(
    "/transcribe",
    summary="Транскрипция аудио (WAV)",
    description="Загрузка WAV-файла, транскрипция через Vosk, сохранение результата в БД."
)
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Эндпоинт для транскрипции аудиофайла.
    Поддерживаемые форматы: WAV 16-bit mono, 8/16/44.1 kHz
    """
    suffix = Path(file.filename).suffix or ".wav"
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            audio_path = tmp.name

        text = transcriber.transcribe(audio_path)
        await WhisperTranscriptDAO.create(
            file_name=file.filename,
            channel_id=None,
            text=text
        )
        return JSONResponse(
            content={"text" : text},
            headers={"X-Transcription-Status": "success"}
        )

    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    finally:
        if 'audio_path' in locals() and Path(audio_path).exists:
            Path(audio_path).unlink(missing_ok=True)
