from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.app.middlewares.translations import LangType


async def new_game(translate: LangType) -> InlineKeyboardMarkup:
    yes_btn = InlineKeyboardButton(text=translate("yes"), callback_data="new_game:yes")
    no_btn = InlineKeyboardButton(text=translate("no"), callback_data="new_game:no")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[yes_btn], [no_btn]])
    return keyboard


async def games_message(translate: LangType):
    completed = InlineKeyboardButton(
        text=translate("completed"), callback_data="games:completed"
    )
    not_completed = InlineKeyboardButton(
        text=translate("not_completed"), callback_data="games:not_completed"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[completed], [not_completed]])
    return keyboard
async def games_response(translate:LangType, page:int):
     keyboard = InlineKeyboardBuilder()
     keyboard.button("previous", callback_data=f'page:{page-1}')
     