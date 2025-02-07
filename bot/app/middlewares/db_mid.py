from database.database import get_async_db
from aiogram.types import Message
from aiogram import BaseMiddleware

from typing import Callable, Awaitable, Dict, Any


class DatabaseMiddleware(BaseMiddleware):
    async def __call__( #type:ignore
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ):
        async for db_session in get_async_db():
            data["db"] = db_session  # Inject database session into data
            try:
                return await handler(event, data)
            finally:
                await db_session.close()
