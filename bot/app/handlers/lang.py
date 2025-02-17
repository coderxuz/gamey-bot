from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from bot.app.keyboards.lang import inline as lang_inline
from bot.app.services.translations.translations import set_user_language
from bot.app.middlewares.translations import TranslationMiddleware
from database.models import User
from bot.app.states.user_state import UserAuth
from bot.app.filters.text_int import TextIn
from bot.app.middlewares.translations import LangType
from bot.app.keyboards.main import reply as main_reply
from bot.app.filters.chat_filter import ChatFilter
from common import ADMIN_ID
from bot.app.keyboards.main.reply import admin_main
from bot.app.keyboards.auth.inline import auth_key

router = Router()
router.message.filter(ChatFilter(chat_type="private"))


@router.message(TextIn(("Til", "Язык", "Language")))
async def change_lang(message: Message, translate: LangType):
    keyboard = await lang_inline.lang_keys()
    choose_lang = (
        "Iltimos tilni tanlang\nPlease select language\nПожалуйста, выберите язык"
    )
    await message.answer(choose_lang, reply_markup=keyboard)


@router.callback_query(F.data == "choose_lang")
async def choose_keys(query: CallbackQuery):
    keyboard = await lang_inline.lang_keys()
    await query.message.edit_reply_markup(reply_markup=keyboard)  # type:ignore


@router.callback_query(F.data.startswith("lang"))
async def lang_choose(
    query: CallbackQuery, db: AsyncSession, state: FSMContext, translate: LangType
):
    lang_code = query.data.split("_")[1]  # type:ignore
    await set_user_language(user_id=query.from_user.id, lang_code=lang_code)
    t = TranslationMiddleware.get_translation
    keyboard = await main_reply.main_keys(translate=translate, lang_code=lang_code)
    db_user = (
        (await db.execute(select(User).where(User.tg_id == query.from_user.id)))
        .scalars()
        .first()
    )
    if db_user and db_user.is_admin == True:
        keyboard = await admin_main(translate=t, lang_code=lang_code)
    if query.from_user.id == ADMIN_ID:
        keyboard = await admin_main(translate=t, lang_code=lang_code, main_admin=True)
    await query.message.answer(
        t(lang_code, "lang_choosen"), reply_markup=keyboard
    )  # type:ignore
    if not db_user:
        await query.message.answer(
            t(lang_code,"please_register"),
            reply_markup=await auth_key(t(lang_code,"authorize")),
        )  # type:ignore
