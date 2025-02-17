from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from aiogram.fsm.context import FSMContext


from bot.app.filters.text_int import TextIn
from bot.app.middlewares.translations import LangType
from database.models import User
from bot.app.keyboards.admin.admin_operation import inline as admin_op_inline
from bot.app.keyboards.admin.admin_operation import reply as admin_op_reply
from bot.app.keyboards.main import reply as main_reply
from common import logger
from bot.app.states.admin import AdminAdd
from bot.app.keyboards.admin.game import reply as game_reply
from common import ADMIN_ID
from bot.app.filters.main_admin import MainAdmin
from bot import bot
from bot.app.middlewares.translations import TranslationMiddleware


import re

router = Router()
router.message.filter(MainAdmin())


@router.message(TextIn(("Админ", "Admin")))
async def show_admin_btns(message: Message, translate: LangType):
    keyboard = await admin_op_reply.admin_btns(translate=translate)
    await message.answer(translate("in_admin"), reply_markup=keyboard)


@router.message(TextIn(("Back", "Админы", "Orqaga")))
async def to_main(message: Message, translate: LangType):
    keyboard = await main_reply.admin_main(translate=translate)
    await message.answer(translate("in_main"), reply_markup=keyboard)


@router.message(TextIn(("Admins", "Adminlar", "Админы")))
async def show_admins(message: Message, translate: LangType, db: AsyncSession):
    page = 1
    admins = (
        (
            await db.execute(
                select(User)
                .where(User.is_admin == True, User.tg_id!=message.from_user.id)
                .limit(10)
                .offset((page - 1) * 10)
            )
        )
        .scalars()
        .all()
    )
    total_pages = len(admins)
    response_txt: str = translate("not_found")
    count = 0
    admin_id_list: list[list[int]] = []
    for admin in admins:
        if count == 0:
            response_txt = ""
        count += 1
        response_txt += (
            f"<b>{count}</b>)<b>{translate('first_name_txt')}</b>. {admin.first_name}\n"
            f"    <b>{translate('last_name_txt')}</b>. {admin.last_name}\n\n"
        )
        admin_id_list.append([count, admin.id])
    keyboard = await admin_op_inline.get_admins(
        translate=translate,
        page=page,
        total_pages=total_pages,
        admin_count_list=admin_id_list,
    )
    await message.answer(text=response_txt, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data.startswith("show_admin"))
async def show_single_admin(
    query: CallbackQuery, translate: LangType, db: AsyncSession
):
    data = query.data.split(":")
    user_id = int(data[1])
    admin = (await db.execute(select(User).where(User.id == user_id))).scalars().first()
    if admin is None:
        await query.message.answer(translate("not_found"))
        return
    response_txt = (
        f"<b>{translate('first_name_txt')}</b>. {admin.first_name}\n"
        f"<b>{translate('last_name_txt')}</b>. {admin.last_name}\n"
        f"<b>{translate('phone_number')}</b>. {admin.phone}\n\n"
    )
    keyboard = await admin_op_inline.delete_admin(translate=translate, user_id=user_id)
    await query.message.answer(response_txt, parse_mode="HTML", reply_markup=keyboard)


@router.callback_query(F.data.startswith("admins"))
async def show_single_admin_pagination(
    query: CallbackQuery, translate: LangType, db: AsyncSession
):
    data = query.data.split(":")  # type:ignore
    page = int(data[1])
    admins = (
        (
            await db.execute(
                select(User)
                .where(User.is_admin == True)
                .limit(10)
                .offset((page - 1) * 10)
            )
        )
        .scalars()
        .all()
    )
    total_pages = len(admins)
    response_txt: str = translate("not_found")
    count = 0
    admin_id_list: list[list[int]] = []
    for admin in admins:
        if count == 0:
            response_txt = ""
        count += 1
        response_txt += (
            f"<b>{count}</b>)<b>{translate('first_name_txt')}</b>. {admin.first_name}\n"
            f"    <b>{translate('last_name_txt')}</b>. {admin.last_name}\n\n"
        )
        admin_id_list.append([count, admin.id])
    keyboard = await admin_op_inline.get_admins(
        translate=translate,
        page=page,
        total_pages=total_pages,
        admin_count_list=admin_id_list,
    )
    await query.message.edit_text(
        text=response_txt, reply_markup=keyboard, parse_mode="HTML"
    )


@router.message(TextIn(("Add admin", "Добавить админа", "Admin qo'shish")))
async def add_admin_btn(message: Message, translate: LangType, state: FSMContext):
    keyboard = await game_reply.game_cancel(translate=translate)
    await message.answer(translate("write_first_name"), reply_markup=keyboard)
    await state.set_state(AdminAdd.user_first_name)


@router.message(AdminAdd.user_first_name)
async def add_admin(message: Message, translate: LangType, db: AsyncSession):
    latin_cyril = r"^[A-Za-zА-Яа-яЁё]+$"
    if not re.match(latin_cyril, message.text):  # type:ignore
        await message.answer(translate("only_letter"))
        return
    page = 1
    db_users = (
        (
            (
                await db.execute(
                    select(User)
                    .where(
                        User.first_name.ilike(f"%{message.text}%"),
                        User.is_admin == False,
                    )
                    .limit(10)
                    .offset((page - 1) * 10)
                )
            )
        )
        .scalars()
        .all()
    )
    total_pages = len(db_users)
    response_txt: str = translate("not_found")
    count = 0
    db_users_id: list[list[int]] = []
    for user in db_users:
        if count == 0:
            response_txt = ""
        count += 1
        response_txt += (
            f"<b>{count}</b>)<b>{translate('first_name_txt')}</b>. {user.first_name}\n"
            f"    <b>{translate('last_name_txt')}</b>. {user.last_name}\n\n"
        )
        db_users_id.append([count, user.id])
    keyboard = await admin_op_inline.add_admins(
        translate=translate,
        user_id_count=db_users_id,
        page=page,
        total_pages=total_pages,
    )
    await message.answer(response_txt, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data.startswith("add_admin"))
async def show_single_user(query: CallbackQuery, translate: LangType, db: AsyncSession):
    data = query.data.split(":")  # type:ignore
    user_id = int(data[1])
    db_user = (
        (
            await db.execute(
                select(User).where(User.id == user_id, User.is_admin == False)
            )
        )
        .scalars()
        .first()
    )
    if db_user is None:
        await query.message.answer(translate("not_found"))
        return
    response_txt = (
        f"<b>{translate('first_name_txt')}</b>. {db_user.first_name}\n"
        f"<b>{translate('last_name_txt')}</b>. {db_user.last_name}\n"
        f"<b>{translate("phone_number")}</b>. {db_user.phone}\n\n"
    )
    keyboard = await admin_op_inline.set_admin(translate=translate, user_id=db_user.id)
    await query.message.answer(
        text=response_txt, reply_markup=keyboard, parse_mode="HTML"
    )
@router.callback_query(F.data.startswith("admin_add_pg"))
async def show_single_user(query: CallbackQuery, translate: LangType, db: AsyncSession):    
    data = query.data.split(":")  # type:ignore
    page = int(data[1])
    admins = (
        (
            await db.execute(
                select(User)
                .where(User.is_admin == True)
                .limit(10)
                .offset((page - 1) * 10)
            )
        )
        .scalars()
        .all()
    )
    total_pages = len(admins)
    response_txt: str = translate("not_found")
    count = 0
    admin_id_list: list[list[int]] = []
    for admin in admins:
        if count == 0:
            response_txt = ""
        count += 1
        response_txt += (
            f"<b>{count}</b>)<b>{translate('first_name_txt')}</b>. {admin.first_name}\n"
            f"    <b>{translate('last_name_txt')}</b>. {admin.last_name}\n\n"
        )
        admin_id_list.append([count, admin.id])
    keyboard = await admin_op_inline.get_admins(
        translate=translate,
        page=page,
        total_pages=total_pages,
        admin_count_list=admin_id_list,
    )
    await query.message.edit_text(
        text=response_txt, reply_markup=keyboard, parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("set_as_admin"))
async def set_as_admin(query: CallbackQuery, translate: LangType, db: AsyncSession):
    data = query.data.split(":")  # type:ignore
    user_id = int(data[1])

    db_user = (
        (
            await db.execute(
                select(User).where(User.id == user_id, User.is_admin == False)
            )
        )
        .scalars()
        .first()
    )
    if db_user is None:
        await query.message.answer(translate("not_found"))
        return
    db_user.is_admin = True
    await db.commit()
    await query.message.answer(
        translate("setted_as_admin").format(
            first_name=db_user.first_name,
            last_name=db_user.last_name,
        ),
        reply_markup= await admin_op_reply.admin_btns(translate=translate),
    )
    user_lang_code = await TranslationMiddleware.get_user_language(user_id=db_user.tg_id)
    t= TranslationMiddleware.get_translation
    await bot.send_message(
        chat_id=db_user.tg_id,
        text=t(user_lang_code, key='you_setted_as_admin'),
        reply_markup=await main_reply.admin_main(translate=t, lang_code=user_lang_code)
    ) if db_user.tg_id else None

@router.callback_query(F.data.startswith("delete_admin"))
async def show_single_admin_pagination(
    query: CallbackQuery, translate: LangType, db: AsyncSession
):
    data = query.data.split(":")  # type:ignore
    user_id = int(data[1])
    
    db_user = (
        (
            await db.execute(
                select(User).where(User.id == user_id, User.is_admin == True)
            )
        )
        .scalars()
        .first()
    )
    if db_user is None:
        await query.message.answer(translate("not_found"))
        return
    db_user.is_admin = False
    await db.commit()
    await query.message.answer(
        translate("deleted_as_admin").format(
            first_name=db_user.first_name,
            last_name=db_user.last_name,
        ),
        reply_markup= await admin_op_reply.admin_btns(translate=translate),
    )
    user_lang_code = await TranslationMiddleware.get_user_language(user_id=db_user.tg_id)
    t= TranslationMiddleware.get_translation
    await bot.send_message(
        chat_id=db_user.tg_id,
        text=t(user_lang_code, key='you_deleted_as_admin'),
        reply_markup=await main_reply.main_keys(translate=translate, lang_code=user_lang_code)
    ) if db_user.tg_id else None
