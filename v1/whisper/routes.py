from fastapi import APIRouter, File, UploadFile, HTTPException
import logging
import tempfile
import os
from .service import WhisperTranscriber
from v1.db.whisper_dao import WhisperTranscriptDAO


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
    return {"status": "whisper ok"}


@router.post(
    "/transcribe",
    summary="Транскрипция аудио (WAV)",
    description="Загрузка WAV-файла, транскрипция через Vosk, сохранение результата в БД."
)
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Эндпоинт для транскрипции аудиофайла (WAV) в текст.
    Сохраняет файл во временное хранилище, передаёт путь в Whisper, удаляет файл после обработки.
    Результат транскрипции сохраняется в БД (whisper_transcripts).
    """
    logger.info("transcribe_audio: старт обработки запроса")
    print("transcribe_audio: старт обработки запроса")
    suffix = os.path.splitext(file.filename)[-1] or ".wav"
    try:
        logger.info(f"transcribe_audio: создаём временный файл с суффиксом {suffix}")
        print(f"transcribe_audio: создаём временный файл с суффиксом {suffix}")
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            file_bytes = await file.read()
            logger.info(f"transcribe_audio: получили {len(file_bytes)} байт из файла {file.filename}")
            print(f"transcribe_audio: получили {len(file_bytes)} байт из файла {file.filename}")
            tmp.write(file_bytes)
            audio_path = tmp.name
        logger.info(f"transcribe_audio: временный файл создан: {audio_path}")
        print(f"transcribe_audio: временный файл создан: {audio_path}")
        text = transcriber.transcribe(audio_path)
        logger.info("transcribe_audio: транскрипция завершена, сохраняем результат в БД")
        print("transcribe_audio: транскрипция завершена, сохраняем результат в БД")
        await WhisperTranscriptDAO.create(file_name=file.filename, channel_id=None, text=text)
        logger.info("transcribe_audio: возвращаем результат клиенту")
        print("transcribe_audio: возвращаем результат клиенту")
        return {"text": text}
    except Exception as e:
        logger.error(f"Ошибка транскрипции: {e}")
        print(f"Ошибка транскрипции: {e}")
        raise HTTPException(status_code=500, detail="Ошибка транскрипции аудио")
    finally:
        if 'audio_path' in locals() and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
                logger.info(f"transcribe_audio: временный файл {audio_path} удалён")
                print(f"transcribe_audio: временный файл {audio_path} удалён")
            except Exception as e:
                logger.warning(f"Не удалось удалить временный файл: {e}")
                print(f"Не удалось удалить временный файл: {e}")
