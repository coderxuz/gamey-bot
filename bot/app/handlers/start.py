from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.app.filters.auth import Registered
from bot.app.keyboards.lang import inline as lang_inline
from bot.app.middlewares.translations import LangType
from bot.app.keyboards.main import reply as main_reply
from bot.app.filters.chat_filter import ChatFilter
from common import ADMIN_ID
from bot.app.keyboards.main.reply import admin_main
from common import logger
from database.models import User

logger.debug(ADMIN_ID)

router = Router()
router.message.filter(ChatFilter(chat_type="private"))


@router.message(CommandStart(), Registered(is_registered=True))
async def hello(message: Message, translate: LangType, db: AsyncSession, state:FSMContext):
    keyboard = await main_reply.main_keys(translate=translate)
    db_user = (
        (
            (
                await db.execute(
                    select(User).where(User.tg_id == message.from_user.id, User.is_admin == True) #type:ignore
                )
            )
        )
        .scalars()
        .first()
    )
    if message.from_user.id == int(ADMIN_ID) or db_user and db_user.is_admin == True: #type:ignore
        keyboard = await admin_main(translate=translate) 
    await message.answer("Hello", reply_markup=keyboard)
    await state.clear()


@router.message(CommandStart())
async def start_not_authorized(
    message: Message, translate: LangType, state: FSMContext
):
    keyboard = await lang_inline.start_inline_dont_sign(translate=translate)
    choose_lang = (
        "Iltimos tilni tanlang\nPlease select language\nПожалуйста, выберите язык"
    )
    await message.answer(choose_lang, reply_markup=keyboard)
    await state.clear()
