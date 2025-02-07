from aiogram.filters import Filter
from aiogram.types import Message

from typing import Tuple


class TextIn(Filter):
    def __init__(self, text_list: list[str]|Tuple[str, ...]):
        self.text_list=text_list 

    async def __call__(self, message: Message) -> bool:
        return message.text in self.text_list
