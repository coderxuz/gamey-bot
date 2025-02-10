from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


from bot.app.filters.chat_filter import ChatFilter
from bot.app.middlewares.translations import LangType
from bot.app.keyboards.main.reply import admin_main
from common import ADMIN_ID


router = Router()
router.message.filter(ChatFilter(chat_type="private"))



@router.message(Command("admin"))
async def admin_command(message: Message, translate: LangType):
    if not ADMIN_ID:
        raise ValueError("Admin id not found")

    if not message.from_user.id == int(ADMIN_ID):  # type:ignore
        return
    keyboard = await admin_main(translate=translate)
    await message.answer(translate("admin_text"), reply_markup=keyboard)



