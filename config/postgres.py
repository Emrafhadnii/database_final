from sqlalchemy.dialects.postgresql.dml import OnConflictDoNothing
from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import Session, registry, sessionmaker
from .settings import settings
from sqlalchemy import create_engine


CONN = {
    "pool_size": 5,
    "max_overflow": 20,
    "pool_timeout": 5,
    "pool_recycle": 3600,
    "echo":True,
    "future":True
}
SESSION = {
    "autocommit": False,
    "autoflush": False,
    "expire_on_commit": True,
}


ASYNC_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)
SYNC_DATABASE_URL = (
    f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

mapper_registry = registry()

async_engine = create_async_engine(ASYNC_DATABASE_URL, **CONN)
sync_engine = create_engine(SYNC_DATABASE_URL, **CONN)

mapper_registry.metadata.create_all(sync_engine, checkfirst=True)


SessionLocal = async_sessionmaker(autocommit=False, 
                                  autoflush=False, 
                                  bind=async_engine, 
                                  class_=AsyncSession,
                                  expire_on_commit=False)

async def get_session():
    async with SessionLocal() as db:
        yield db

