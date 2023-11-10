from settings import Settings
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker


async def async_db() -> AsyncSession:
    engine = create_async_engine(Settings.sql_dsn)

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    with async_session() as session:
        yield session


def sync_db() -> Session:
    engine = create_engine(Settings.sql_dsn)

    session = sessionmaker(engine, expire_on_commit=False)

    return session()
