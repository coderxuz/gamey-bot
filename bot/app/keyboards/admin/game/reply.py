from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.app.middlewares.translations import LangType


async def game_cancel(translate: LangType) -> ReplyKeyboardMarkup:
    cancel = KeyboardButton(text=translate("cancel"))

    keyboard = ReplyKeyboardMarkup(keyboard=[[cancel]], resize_keyboard=True)
    
    return keyboard
