from aiogram import Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.app.filters.auth import Registered
from bot.app.middlewares.translations import LangType
from bot.app.states.user_state import UserAuth
from bot.app.keyboards.auth import reply as auth_reply
from database.models import User
from bot.app.keyboards.main import reply as main_reply
from bot.app.filters.chat_filter import ChatFilter

import re

router = Router()
router.message.filter(ChatFilter(chat_type='private'))

@router.message(UserAuth.first_name)
async def set_first_name(message: Message, state: FSMContext, translate: LangType):
    latin_cyril = r"^[A-Za-zА-Яа-яЁё]+$"
    if not re.match(latin_cyril, message.text):  # type:ignore
        await message.answer(translate("only_letter"))
        return
    await state.update_data(first_name=message.text.capitalize())  # type:ignore
    await message.answer(translate("last_name"))
    await state.set_state(UserAuth.last_name)


@router.message(UserAuth.last_name)
async def set_last_name(message: Message, state: FSMContext, translate: LangType):
    latin_cyril = r"^[A-Za-zА-Яа-яЁё]+$"
    if not re.match(latin_cyril, message.text):  # type:ignore
        await message.answer(translate("only_letter"))
        return
    await state.update_data(last_name=message.text.capitalize())  # type:ignore
    keyboard = await auth_reply.send_phone(translate=translate)
    await message.answer(translate("phone"), reply_markup=keyboard)
    await state.set_state(UserAuth.phone)


@router.message(UserAuth.phone)
async def set_phone(
    message: Message, state: FSMContext, translate: LangType, db: AsyncSession
):
    user_data = await state.get_data()
    if message.contact.user_id != message.from_user.id: #type:ignore
        await message.answer(translate("phone"))
        return
    phone_number = (
        message.contact.phone_number  # type:ignore
        if message.contact.phone_number.startswith("+")  # type:ignore
        else f"+{message.contact.phone_number}"  # type:ignore
    )
    new_user = User(
        first_name=user_data.get("first_name"),
        last_name=user_data.get("last_name"),
        phone=phone_number,
        tg_id=message.from_user.id,  # type:ignore
    )
    db.add(new_user)
    await db.commit()
    keyboard = await main_reply.main_keys(translate=translate)
    await message.answer(translate("registered"), reply_markup=keyboard)
    await state.clear()


@router.message(Registered(is_registered=False))
async def please_register(message: Message, state: FSMContext, translate: LangType):
    await message.answer(translate("please_register"))
    await message.answer(translate("first_name"), reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserAuth.first_name)


@router.callback_query(Registered(is_registered=False))
async def please_register_query(
    query: CallbackQuery, translate: LangType, state: FSMContext
):
    await query.message.answer(translate("please_register"))  # type:ignore
    await query.message.answer(translate("first_name"))  # type:ignore
    await state.set_state(UserAuth.first_name)
