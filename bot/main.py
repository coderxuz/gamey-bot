import asyncio
import logging

from bot import dp, bot
from bot.app.handlers import start, lang, auth, group
from bot.app.middlewares.translations import TranslationMiddleware
from bot.app.middlewares.db_mid import DatabaseMiddleware

dp.message.middleware(TranslationMiddleware)
dp.callback_query.middleware(TranslationMiddleware)
dp.message.middleware(DatabaseMiddleware())
dp.callback_query.middleware(DatabaseMiddleware())
async def main():
    dp.include_router(start.router)
    dp.include_router(lang.router)
    dp.include_router(auth.router)
    dp.include_router(group.router)
    await dp.start_polling(bot)  # type:ignore


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.DEBUG)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Finish")