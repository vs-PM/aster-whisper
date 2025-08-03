from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import make_url

from v1.config.db_config import db_settings

Base = declarative_base()

# Явное преобразование строки в URL для SQLAlchemy
database_url = make_url(db_settings.DATABASE_URL)

engine = create_async_engine(
    database_url,
    echo=False,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600
)

async_session_maker = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)