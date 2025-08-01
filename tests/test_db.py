import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.exc import OperationalError
import asyncio

from v1.db import DATABASE_URL

@pytest.mark.asyncio
async def test_db_connection():
    engine = create_async_engine(DATABASE_URL, echo=False)
    try:
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
    except OperationalError as e:
        pytest.fail(f"DB connection failed: {e}")
    finally:
        await engine.dispose()
