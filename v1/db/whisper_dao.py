from . import async_session_maker
from .whisper_models import VoskText

class WhisperTranscriptDAO:
    @staticmethod
    async def create(file_name: str, channel_id: str, text: str, created_at=None):
        async with async_session_maker() as session:
            obj = VoskText(file_name=file_name, channel_id=channel_id, text=text, created_at=created_at)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj

    @staticmethod
    async def get_by_id(id_: int):
        async with async_session_maker() as session:
            result = await session.execute(
                VoskText.__table__.select().where(VoskText.id == id_)
            )
            row = result.first()
            return row
