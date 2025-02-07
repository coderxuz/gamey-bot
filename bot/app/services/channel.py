from bot import bot
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from dotenv import load_dotenv

from os import getenv


load_dotenv()
CHANNEL_ID = getenv("CHANNEL_ID")
if not CHANNEL_ID:
    raise ValueError("Channel_id didn't find")


async def is_subscribed(message: Message) -> bool:
    try:
        chat_member = await bot.get_chat_member(
            chat_id=CHANNEL_ID, user_id=message.from_user.id
        )
        return chat_member.status in ["member", "administrator", "creator"]
    except TelegramBadRequest:  # If user isn't found in the channel
        return False
