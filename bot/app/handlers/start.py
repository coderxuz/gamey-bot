from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from bot.app.filters.auth import Registered
from bot.app.keyboards.lang import inline as lang_inline
from bot.app.middlewares.translations import LangType
from bot.app.states.user_state import UserAuth
from bot.app.keyboards.main import reply as main_reply
from bot.app.filters.chat_filter import ChatFilter

router = Router()
router.message.filter(ChatFilter(chat_type='private'))

@router.message(CommandStart(), Registered(is_registered=True))
async def hello(message: Message, translate:LangType):
     keyboard = await main_reply.main_keys(translate=translate)
     await message.answer("Hello", reply_markup=keyboard)


@router.message(CommandStart())
async def start_not_authorized(message: Message, translate: LangType, state:FSMContext):
    keyboard = await lang_inline.start_inline_dont_sign(translate=translate)
    choose_lang = (
        "Iltimos tilni tanlang\nPlease select language\nПожалуйста, выберите язык"
    )
    await message.answer(choose_lang, reply_markup=keyboard)
    await message.answer(translate('first_name'), reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserAuth.first_name)
