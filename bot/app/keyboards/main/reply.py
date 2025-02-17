from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.app.middlewares.translations import LangType, TranslationCallable

import inspect
from typing import Optional


async def main_keys(
    translate: LangType , lang_code: Optional[str] = None
) -> ReplyKeyboardMarkup:
    # Use `get_text` for translations
    group = KeyboardButton(text=translate("group",lang_code))
    channel = KeyboardButton(text=translate("channel",lang_code))
    lang = KeyboardButton(text=translate("lang",lang_code))

    return ReplyKeyboardMarkup(
        keyboard=[[group, channel], [lang]], resize_keyboard=True
    )


async def admin_main(
    translate: LangType ,
    lang_code: Optional[str] = None,
    main_admin: bool = False,
):

    new_game = KeyboardButton(text=translate("new_game",lang_code))
    lang = KeyboardButton(text=translate("lang",lang_code))
    games = KeyboardButton(text=translate("games",lang_code))
    admin = KeyboardButton(text=translate("admin",lang_code))

    return ReplyKeyboardMarkup(
        keyboard=(
            [[new_game, games], [lang, admin]]
            if main_admin == True
            else [[new_game, games], [lang]]
        ),
        resize_keyboard=True,
    )
