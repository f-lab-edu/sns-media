from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, pool
from sqlmodel.ext.asyncio.session import AsyncSession

from src import config

if "sqlite+aiosqlite:///:memory:" in config.db.url:
    engine = create_async_engine(
        url=config.db.url,
        echo=config.db.echo,
        connect_args={
            "check_same_thread": False,
        },
        poolclass=pool.StaticPool,
    )
else:
    engine = create_async_engine(
        url=config.db.url,
        echo=config.db.echo,
        pool_size=50,
        max_overflow=30,
        pool_pre_ping=True,
    )


async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db() -> None:
    await engine.dispose()
