from . import async_session_maker
from .whisper_models import WhisperTranscript

class WhisperTranscriptDAO:
    @staticmethod
    async def create(file_name: str, channel_id: str, text: str, created_at=None):
        async with async_session_maker() as session:
            obj = WhisperTranscript(file_name=file_name, channel_id=channel_id, text=text, created_at=created_at)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj

    @staticmethod
    async def get_by_id(id_: int):
        async with async_session_maker() as session:
            result = await session.execute(
                WhisperTranscript.__table__.select().where(WhisperTranscript.id == id_)
            )
            row = result.first()
            return row
