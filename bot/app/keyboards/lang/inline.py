from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

from bot.app.middlewares.translations import LangType

async def start_inline_dont_sign(translate:LangType)->InlineKeyboardMarkup:
    lang = InlineKeyboardButton(text=translate('lang'), callback_data='choose_lang')
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[lang]]
    )
    
    return keyboard

async def lang_keys()->InlineKeyboardMarkup:
    uzbek = InlineKeyboardButton(text="O'zbek", callback_data='lang_uz')
    rus = InlineKeyboardButton(text="Русский", callback_data='lang_ru')
    english = InlineKeyboardButton(text="English", callback_data='lang_en')
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[uzbek],[english,rus]]
    )
    
    return keyboard