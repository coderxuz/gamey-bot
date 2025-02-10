from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.app.filters.text_int import TextIn
from bot.app.middlewares.translations import LangType
from database.models import Game
from bot.app.keyboards.admin.game import inline as game_inline
from common import logger

import asyncio


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
    is_completed = bool(query.data.split(":")[1])
    
    page = 1
    games = (
            (
                await db.execute(
                    select(Game)
                    .where(Game.is_completed == is_completed)
                    .limit(10)
                    .offset((page - 1) * 10)
                )
            )
            .scalars()
            .all()
        )
    total_pages = len(games)
    response_txt: str = ""
    count = 0
    for game in games:
        count += 1
        response_txt += (
                f"{count}){translate('created_at')}: {game.created_at.strftime('%m-%d-%Y')}\n"
                f"{translate('end_time')}: {game.updated_at.strftime('%m-%d-%Y')}\n\n\n"
            )
    keyboard = await game_inline.games_response(
            translate=translate, page=page, total_pages=total_pages, completed=True
        )
    await query.message.edit_text(text=response_txt, reply_markup=keyboard)


@router.callback_query(F.data.startswith("page"))
async def pagination_btns(query: CallbackQuery, translate: LangType, db: AsyncSession):
    data = query.data.split(":")
    page = int(data[2])
    completed = bool(data[1])
    games = (
        (
            await db.execute(
                select(Game)
                .where(Game.is_completed == completed)
                .limit(10)
                .offset((page - 1) * 10)
            )
        )
        .scalars()
        .all()
    )
    total_pages = len(games)
    response_txt: str = ""
    count = 0
    for game in games:
        count += 1
        response_txt += (
                f"{count}){translate('created_at')}: {game.created_at.strftime('%m-%d-%Y')}\n"
                f"{translate('end_time')}: {game.updated_at.strftime('%m-%d-%Y')}\n\n\n"
            )
    keyboard = await game_inline.games_response(
            translate=translate, page=page, total_pages=total_pages, completed=completed
        )
    await query.message.edit_text(text=response_txt, reply_markup=keyboard)
