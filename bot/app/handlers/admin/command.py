from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from bot.app.filters.chat_filter import ChatFilter
from bot.app.middlewares.translations import LangType
from bot.app.keyboards.main.reply import admin_main
from common import ADMIN_ID
from database.models import User


router = Router()
router.message.filter(ChatFilter(chat_type="private"))



@router.message(Command("admin"))
async def admin_command(message: Message, translate: LangType, db:AsyncSession):
    if not ADMIN_ID:
        raise ValueError("Admin id not found")
    db_user = (
        (await db.execute(select(User).where(User.tg_id == message.from_user.id)))
        .scalars()
        .first()
    )
    if message.from_user.id != ADMIN_ID or not db_user:  # type:ignore
        return
    db_user.is_admin = True
    await db.commit()
    keyboard = await admin_main(translate=translate)
    await message.answer(translate("admin_text"), reply_markup=keyboard)



