from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from database import Base, engine

from datetime import datetime
from typing import List


class User(Base):
    __tablename__ = "users"

    first_name: Mapped[str]
    last_name: Mapped[str]
    phone: Mapped[str] = mapped_column(unique=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    is_admin:Mapped[bool] = mapped_column(server_default='false')
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    games: Mapped[List["UserGame"]] = relationship(back_populates="user")


class Game(Base):
    __tablename__ = "games"
    
    name:Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    is_completed:Mapped[bool] = mapped_column(server_default='false')
    users: Mapped[List["UserGame"]] = relationship(back_populates="game")


class UserGame(Base):
    __tablename__ = "user_game"

    user_tg_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.tg_id"))
    is_paid:Mapped[bool] = mapped_column(server_default='false')
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))

    user: Mapped["User"] = relationship(back_populates="games")
    game: Mapped["Game"] = relationship(back_populates="users")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
