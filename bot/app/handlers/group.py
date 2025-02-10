from aiogram import Router
from aiogram.types import Message

from bot.app.filters.text_int import TextIn
from bot.app.keyboards.group import inline as group_inline
from bot.app.middlewares.translations import LangType
from bot.app.filters.chat_filter import ChatFilter


router = Router()
router.message.filter(ChatFilter(chat_type='private'))

@router.message(TextIn(('Group',"Группа", "Guruh")))
async def invite_group(message:Message, translate:LangType):
     keyboard = await group_inline.join_group(translate=translate)
     await message.answer(translate('group'), reply_markup=keyboard)