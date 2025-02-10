from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.app.filters.text_int import TextIn
from bot.app.middlewares.translations import LangType
from database.models import Game

from bot.app.keyboards.admin.game import inline as game_inline


router = Router()


@router.message(TextIn(("New game", "Новая игра", "Yangi o'yin")))
async def new_game(message: Message, translate: LangType):
    keyboard = await game_inline.new_game(translate=translate)
    await message.answer(translate("new_game_request"), reply_markup=keyboard)


@router.callback_query(F.data.startswith("new_game"))
async def new_game_response(
    query: CallbackQuery, translate: LangType, db: AsyncSession
):
    response = query.data.split(":")[1]  # type:ignore
    if response == "yes":
        new_game_db = Game()
        db.add(new_game_db)
        await db.commit()
        await query.answer(translate("new_game_created"), show_alert=True)
        await query.message.answer(translate("new_game_created"))  # type:ignore
        await query.message.delete()  # type:ignore
        return
    await query.message.delete()  # type:ignore


@router.message(TextIn(("Games", "Игры", "O'yinlar")))
async def show_games(message: Message, translate: LangType):
    keyboard = await game_inline.games_message(translate=translate)
    await message.answer(translate("choose_completed"), reply_markup=keyboard)


@router.callback_query(F.data.startswith("games"))
async def get_games(query: CallbackQuery, translate: LangType, db: AsyncSession):
    response = query.data.split(":")[1]
    if response == "completed":
        games = (
            (await db.execute(select(Game).where(Game.is_completed == True)))
            .scalars()
            .all()
        )
        
