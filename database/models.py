from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from database import Base, engine

from datetime import datetime


class User(Base):
    __tablename__ = "users"

    first_name: Mapped[str]
    last_name: Mapped[str]
    phone: Mapped[str] = mapped_column(unique=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)