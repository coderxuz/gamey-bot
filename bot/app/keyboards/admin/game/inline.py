from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.app.middlewares.translations import LangType

from typing import List


async def games_message(translate: LangType):
    completed = InlineKeyboardButton(
        text=translate("completed"), callback_data=f"games:{True}"
    )
    not_completed = InlineKeyboardButton(
        text=translate("not_completed"), callback_data=f"games:{False}"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[completed], [not_completed]])
    return keyboard


async def games_response(
    translate: LangType,
    page: int,
    total_pages: int,
    completed: bool,
    game_id_list: List[list[int]],
):
    keyboard = InlineKeyboardBuilder()

    for count, id in game_id_list:
        keyboard.button(text=str(count), callback_data=f"get_game:{id}")
    if len(game_id_list) > 5:
        keyboard.adjust(5)
    if page > 0 and page != 1:
        prev_btn = InlineKeyboardButton(
            text="previous", callback_data=f"page:{completed}:{page-1}"
        )
        keyboard.row(prev_btn)
    if page < total_pages - 1:
        next_btn = InlineKeyboardButton(
            text="Next", callback_data=f"page:{completed}:{page+1}"
        )
        keyboard.row(next_btn)

    return keyboard.as_markup()


async def single_game(translate: LangType, game_id: int):
    add_player = InlineKeyboardButton(
        text=translate("add_player"), callback_data=f"add_user:{game_id}"
    )
    complete_game = InlineKeyboardButton(
        text=translate("complete_game"), callback_data=f"complete_game:{game_id}"
    )
    
    return InlineKeyboardMarkup(
        inline_keyboard=[[add_player], [complete_game]]
    )

async def join_game(translate:LangType, game_id:int):
    yes_btn = InlineKeyboardButton(
        text=translate("yes"), callback_data=f"join_game:{game_id}"
    )
    no_btn = InlineKeyboardButton(
        text=translate("no"), callback_data=f"join_game"
    )
    
    return InlineKeyboardMarkup(
        inline_keyboard=[[yes_btn], [no_btn]]
    )
async def add_game(translate:LangType,user_lang:str, game_id:int,user_id:int):
    yes_btn = InlineKeyboardButton(
        text=translate("yes", user_lang), callback_data=f"add_game:{game_id}:{user_id}"
    )
    no_btn = InlineKeyboardButton(
        text=translate("no",user_lang), callback_data=f"add_game"
    )
    
    return InlineKeyboardMarkup(
        inline_keyboard=[[yes_btn], [no_btn]]
    )