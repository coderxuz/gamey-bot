from aiogram import Router
from aiogram.types import Message

from bot.app.filters.text_int import TextIn
from bot.app.keyboards.group import inline as group_inline
from bot.app.middlewares.translations import LangType
from bot.app.services.channel import is_subscribed

router = Router()

@router.message(TextIn(('Group',"Группа", "Guruh")))
async def invite_group(message:Message, translate:LangType):
     subscribed = await is_subscribed(message=message)
     keyboard = await group_inline.join_group(translate=translate)
     await message.answer(f"{subscribed}", reply_markup=keyboard)