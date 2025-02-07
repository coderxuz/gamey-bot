from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.app.middlewares.translations import LangType


async def send_phone(translate: LangType) -> ReplyKeyboardMarkup:
    phone = KeyboardButton(text=translate("share_phone"), request_contact=True)

    keyboard = ReplyKeyboardMarkup(keyboard=[[phone]], resize_keyboard=True)
    return keyboard
