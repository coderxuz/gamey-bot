from aiogram.filters import Filter
from aiogram.types import Message

from typing import Tuple, Literal

ChatType = Literal["private", "group", "supergroup", "channel"]


class ChatFilter(Filter):
    def __init__(self, chat_type:ChatType):
        self.chat_type = chat_type
    async def __call__(self, message: Message) -> bool:
        return self.chat_type == message.chat.type