from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import text

from src.core.config import postgres_settings as pg

Base = declarative_base()

dsn = f"postgresql+asyncpg://{pg.user}:{pg.password}@{pg.host}:{pg.port}/{pg.db}"

engine = create_async_engine(dsn, echo=pg.echo, future=True)
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def create_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def purge_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.execute(text("DROP TYPE IF EXISTS roletype;"))  # TODO remove this
