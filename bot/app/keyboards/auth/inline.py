from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

from bot.app.middlewares.translations import LangType


async def auth_key(auth_txt:str)->InlineKeyboardMarkup:
    auth = InlineKeyboardButton(text=auth_txt, callback_data="authorize")
    return InlineKeyboardMarkup(inline_keyboard=[[auth]])
