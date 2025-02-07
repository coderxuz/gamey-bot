from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.app.middlewares.translations import LangType

group_link = 'https://t.me/+qsooRb0m4bQzNDEy'

async def join_group(translate:LangType)->InlineKeyboardMarkup:
     group_btn = InlineKeyboardButton(text=translate('group'), url=group_link)
     
     keyboard = InlineKeyboardMarkup(
          inline_keyboard=[[group_btn]]
     )
     return keyboard