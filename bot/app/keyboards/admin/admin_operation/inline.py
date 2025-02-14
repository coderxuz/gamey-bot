from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.app.middlewares.translations import LangType


async def get_admins(
    translate: LangType, admin_count_list: list[list[int]], page: int, total_pages: int
):
    builder = InlineKeyboardBuilder()

    for count, user_id in admin_count_list:
        builder.button(text=str(count), callback_data=f"show_admin:{user_id}")
    if len(admin_count_list) > 5:
        builder.adjust(5)
    if page > 0 and page != 1:
        prev_btn = InlineKeyboardButton(
            text="previous", callback_data=f"admins:{page-1}"
        )
        builder.row(prev_btn)
    if page < total_pages - 1:
        next_btn = InlineKeyboardButton(
            text="Next", callback_data=f"admins:{page+1}"
        )
        builder.row(next_btn)
    
    return builder.as_markup()

async def add_admins(
    translate: LangType, user_id_count: list[list[int]], page: int, total_pages: int
):
    builder = InlineKeyboardBuilder()

    for count, user_id in user_id_count:
        builder.button(text=str(count), callback_data=f"add_admin:{user_id}")
    if len(user_id_count) > 5:
        builder.adjust(5)
    if page > 0 and page != 1:
        prev_btn = InlineKeyboardButton(
            text="previous", callback_data=f"admin_add_pg:{page-1}"
        )
        builder.row(prev_btn)
    if page < total_pages - 1:
        next_btn = InlineKeyboardButton(
            text="Next", callback_data=f"admin_add_pg:{page+1}"
        )
        builder.row(next_btn)
    
    return builder.as_markup()

async def set_admin(translate:LangType, user_id:int):
    set_admin_key = InlineKeyboardButton(text=translate("set_as_admin"), callback_data=f"set_as_admin:{user_id}")
    
    return InlineKeyboardMarkup(
        inline_keyboard=[[set_admin_key]]
    )
async def delete_admin(translate:LangType, user_id:int):
    delete_admin_key = InlineKeyboardButton(text=translate("delete_admin"), callback_data=f"delete_admin:{user_id}")
    
    return InlineKeyboardMarkup(
        inline_keyboard=[[delete_admin_key]]
    )