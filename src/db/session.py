from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.db.base import engine

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
