from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.app.middlewares.translations import LangType, TranslationCallable

import inspect
from typing import Optional


async def main_keys(
    translate: LangType | TranslationCallable, lang_code: Optional[str] = None
) -> ReplyKeyboardMarkup:
    num_params = len(inspect.signature(translate).parameters)
    get_text = None
    if num_params == 1:
        get_text = translate  # Directly use for `key`
    elif num_params == 2:
        get_text = lambda key: translate(
            lang_code if lang_code else "ru", key
        )  # Assume first argument is language

    # Use `get_text` for translations
    group = KeyboardButton(text=get_text("group"))
    channel = KeyboardButton(text=get_text("channel"))
    lang = KeyboardButton(text=get_text("lang"))

    return ReplyKeyboardMarkup(
        keyboard=[[group, channel], [lang]], resize_keyboard=True
    )


async def admin_main(translate: LangType|TranslationCallable, lang_code:Optional[str]=None):
    num_params = len(inspect.signature(translate).parameters)
    get_text = None
    if num_params == 1:
        get_text = translate  # Directly use for `key`
    elif num_params == 2:
        get_text = lambda key: translate(
            lang_code if lang_code else "ru", key
        )  # Assume first argument is language
    
    new_game = KeyboardButton(text=get_text("new_game"))
    users = KeyboardButton(text=get_text("users"))
    lang = KeyboardButton(text=get_text("lang"))
    games = KeyboardButton(text=get_text('games'))

    return ReplyKeyboardMarkup(
        keyboard=[[new_game, games], [users,lang]], resize_keyboard=True
    )
