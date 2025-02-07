from typing import Any
from aiogram.filters import Filter
from aiogram.types import Message
from sqlalchemy import select

from database.database import get_async_db
from database.models import User


class Registered(Filter):
    def __init__(self,is_registered: bool = True) -> None:
        self.is_registered:bool = is_registered
    async def __call__(self, msg: Message) -> Any:
        db_user = None
        async for session in get_async_db():
            db_user = (
                (
                    await session.execute(
                        select(User.tg_id).where(User.tg_id == msg.from_user.id)
                    )
                )
                .scalars()
                .first()
            )
        if self.is_registered == False:
            return False if db_user else True
        return True if db_user else False
