from . import async_session_maker
from .docx_models import MfgBot


class MfgBotDAO:
    @staticmethod
    async def get_by_id(id_: int):
        async with async_session_maker() as session:
            result = await session.execute(
                MfgBot.__table__.select().where(MfgBot.id == id_)
            )
            row = result.first()
            return row

    @staticmethod
    async def update_audio_text(id_: int, text: str):
        async with async_session_maker() as session:
            await session.execute(
                MfgBot.__table__.update().where(MfgBot.id == id_).values(audio_text=text)
            )
            await session.commit()
