from collections.abc import AsyncIterator

from sqlalchemy import Enum
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.modules.core.settings import get_settings

settings = get_settings()


class BaseModel(DeclarativeBase):
    pass


class IdMixin:
    id: Mapped[int] = mapped_column(primary_key=True)


engine = create_async_engine(settings.database.url, echo=settings.debug)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)


async def get_db() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session


def make_enum(enum_class, name):
    return Enum(enum_class, name=name, values_callable=lambda e: [m.value for m in e])
