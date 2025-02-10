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
        text=translate("completed"), callback_data="games:{True}"
    )
    not_completed = InlineKeyboardButton(
        text=translate("not_completed"), callback_data="games:{False}"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[completed], [not_completed]])
    return keyboard


async def games_response(translate: LangType, page: int, total_pages:int, completed: bool):
    keyboard = InlineKeyboardBuilder()
    if page > 0:
        keyboard.button(text="previous", callback_data=f"page:{completed}:{page-1}")
    if page<total_pages-1:
        keyboard.button(text="Next", callback_data=f"page:{completed}:{page+1}")
    return keyboard.as_markup()


