from dotenv import load_dotenv

from bot import dp, bot
from bot.app.handlers import start, lang, auth, group, channel, admin
from bot.app.middlewares.translations import TranslationMiddleware
from bot.app.middlewares.db_mid import DatabaseMiddleware

import asyncio
import logging
from os import getenv

dp.message.middleware(TranslationMiddleware)
dp.callback_query.middleware(TranslationMiddleware)
dp.message.middleware(DatabaseMiddleware())
dp.callback_query.middleware(DatabaseMiddleware())

load_dotenv()
DEV_ID = getenv("DEV_ID")


@dp.startup()
async def start_up():
    if not DEV_ID:
        raise ValueError("DEV_ID not found")

    await bot.send_message(chat_id=DEV_ID, text="bot started")


@dp.shutdown()
async def shut_down():
    if not DEV_ID:
        raise ValueError("DEV_ID not found")

    await bot.send_message(chat_id=DEV_ID, text="bot stopped")


async def main():
    dp.include_router(start.router)
    dp.include_router(lang.router)
    dp.include_router(auth.router)
    dp.include_router(channel.router)
    dp.include_router(group.router)
    dp.include_router(admin.router)
    await dp.start_polling(bot)  # type:ignore


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.DEBUG)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Finish")
