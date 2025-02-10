from aiogram.filters import Filter
from aiogram.types import Message

from bot.app.services.channel import is_subscribed


class IsNotSubscribed(Filter):
    async def __call__(self, msg: Message) -> bool:
        return not await is_subscribed(message=msg)
