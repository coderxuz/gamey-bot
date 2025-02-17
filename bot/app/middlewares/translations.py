from aiogram.types import Message, CallbackQuery, Update
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from typing import Dict, Any
from database.redis import get_redis
from bot.app.services.translations.translations import load_translations
from common import logger

from typing import Callable

LangType = Callable[[str], str]
TranslationCallable = Callable[[str, str], str]


class RedisTranslationMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.translations = load_translations()
    
    async def __call__(self, handler,event:Update, data: Dict[str,Any]): #type:ignore
        
        user_id = None
        
        if isinstance(event, Message):
            user_id = event.from_user.id #type:ignore
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
            
        if user_id:
            user_language = await self.get_user_language(user_id)
            data["translate"] = lambda key, lang_code=None: self.get_translation(user_language if not lang_code else lang_code, key) #type:ignore

        return await handler(event, data)
    
    async def get_user_language(self, user_id: int) -> str:
        """
        Retrieve the user's language preference from Redis.
        Defaults to 'en' if not set.
        """
        redis = await get_redis()
        language = await redis.get(f"user:{user_id}:language")
        return language or "ru"  # Default language

    def get_translation(self, lang: str, key: str) -> str:
        """
        Retrieve a translation for the given language and key.
        Fallback to 'en' or 'ru' if the key is not found.
        """
        translation = self.translations.get(lang, {}).get(key, self.translations["ru"].get(key))
        if not translation:
            logger.warning(f"Missing translation for key '{key}' in language '{lang}'. Fallback to 'ru'.")
        return translation #type:ignore
    async def on_pre_process_message(
        self, message: Message, data: Dict[str, Any]
    ) -> None:
        """
        Inject the `translate` function for message handling.
        """
        user_language = await self.get_user_language(message.from_user.id) #type:ignore
        data["translate"] = lambda key: self.get_translation(user_language, key) #type:ignore

    async def on_pre_process_callback_query(
        self, callback_query: CallbackQuery, data: Dict[str, Any]
    ) -> None:
        """
        Inject the `translate` function for callback query handling.
        """
        user_language = await self.get_user_language(callback_query.from_user.id)
        data["translate"] = lambda key: self.get_translation(user_language, key) #type:ignore

TranslationMiddleware = RedisTranslationMiddleware()

async def translate_out_bot(user_id:int, key:str)->str:
        if not user_id:
                raise ValueError('user_id not found')
        
        user_lang = await TranslationMiddleware.get_user_language(user_id=user_id)
        translation = TranslationMiddleware.get_translation(lang=user_lang, key=key)
        
        return translation