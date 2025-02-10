from aiogram import Router
from aiogram.types import Message


from bot.app.filters.channel import IsNotSubscribed
from bot.app.filters.text_int import TextIn
from bot.app.middlewares.translations import LangType
from bot.app.keyboards.channel.inline import channel_btn

router = Router()

@router.message(IsNotSubscribed())
async def subscribe(message:Message, translate:LangType):
     keyboard = await channel_btn(translate=translate)
     await message.answer(translate('channel_subscribe'), reply_markup=keyboard)
@router.message(TextIn(('Channel', 'Канал', 'Kanal')))
async def channel_btn_answer(message:Message, translate:LangType):
     keyboard = await channel_btn(translate=translate)
     await message.answer(translate('channel'), reply_markup=keyboard)