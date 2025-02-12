from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from dotenv import load_dotenv

from common import logger


from os import getenv

load_dotenv()

DB_URL = getenv('DB_URL')

if not DB_URL:
    raise ValueError("DB_URL didn't find")
engine = create_engine(DB_URL)

ASYNC_DB_URL = getenv("ASYNC_DB_URL")
if not ASYNC_DB_URL:
    raise ValueError("ASYNC_DB_URL didn't find")

async_engine = create_async_engine(ASYNC_DB_URL)

SessionLocal = sessionmaker(bind=engine)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.warning(f"Session error \n {e}")
            raise
        finally:
            await session.close()
