from typing import Any
from aiogram.filters import Filter
from aiogram.types import Message
from sqlalchemy import select

from database.database import get_async_db
from database.models import User

from typing import Optional


class Registered(Filter):
    def __init__(self,is_registered:Optional[bool] = True, is_admin:Optional[bool]= None) -> None:
        self.is_registered:Optional[bool] = is_registered
        self.is_admin:Optional[bool] = is_admin
    async def __call__(self, msg: Message) -> Any:
        db_user = None
        async for session in get_async_db():
            db_user = (
                (
                    await session.execute(
                        select(User).where(User.tg_id == msg.from_user.id)
                    )
                )
                
            ).scalars().first()
        if self.is_registered is not None:
            if self.is_registered == False:
                return False if db_user else True
            return True if db_user else False
        if self.is_admin is not None:
            if db_user is None:
                return False
            return db_user.is_admin
        return True if db_user else False
