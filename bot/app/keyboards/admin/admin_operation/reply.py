from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.app.middlewares.translations import LangType


async def admin_btns(translate: LangType):
    add_admin = KeyboardButton(text=translate("add_admin"))
    admins = KeyboardButton(text=translate("admins"))
    back = KeyboardButton(text=translate('back'))

    return ReplyKeyboardMarkup(keyboard=[[add_admin, admins],[back]], resize_keyboard=True)
