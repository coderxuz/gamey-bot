from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.app.middlewares.translations import LangType


async def channel_btn(translate: LangType) -> InlineKeyboardMarkup:
    channel_btn = InlineKeyboardButton(
        text=translate("channel"), url="https://t.me/xursands_blog"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[channel_btn]])

    return keyboard
