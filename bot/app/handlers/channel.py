from aiogram import Router
from aiogram.types import Message, CallbackQuery


from bot.app.filters.channel import IsNotSubscribed
from bot.app.filters.text_int import TextIn
from bot.app.middlewares.translations import LangType
from bot.app.keyboards.channel.inline import channel_btn

router = Router()

@router.message(IsNotSubscribed())
async def subscribe(message:Message, translate:LangType):
     keyboard = await channel_btn(translate=translate)
     await message.answer(translate('channel_subscribe'), reply_markup=keyboard)
@router.callback_query(IsNotSubscribed())
async def subscribe_inline(query:CallbackQuery, translate:LangType):
     keyboard = await channel_btn(translate=translate)
     await query.message.answer(translate('channel_subscribe'), reply_markup=keyboard) #type:ignore
@router.message(TextIn(('Channel', 'Канал', 'Kanal')))
async def channel_btn_answer(message:Message, translate:LangType):
     keyboard = await channel_btn(translate=translate)
     await message.answer(translate('channel'), reply_markup=keyboard)