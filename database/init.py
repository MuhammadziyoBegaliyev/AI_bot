# path: database/__init__.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import settings

engine = create_async_engine(settings.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://"))
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase): pass

async def init_db():
    from .models import User, Drug, Pharmacy, SearchLog, Feedback
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
