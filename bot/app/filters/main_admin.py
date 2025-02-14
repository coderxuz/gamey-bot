from aiogram.filters import Filter
from aiogram.types import Message

from common import ADMIN_ID


class MainAdmin(Filter):

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == ADMIN_ID
