from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.app.filters.text_int import TextIn
from bot.app.middlewares.translations import LangType
from database.models import Game
from bot.app.keyboards.admin.game import inline as game_inline
from bot.app.keyboards.admin.game import reply as game_reply
from bot.app.keyboards.main import reply as main_reply
from bot.app.keyboards.admin.admin_operation import reply as admin_op_reply
from bot.app.states.game import GameState
from common import logger



router = Router()


@router.message(TextIn(("New game", "Новая игра", "Yangi o'yin")))
async def new_game(message: Message, translate: LangType, state: FSMContext):
    keyboard = await game_reply.game_cancel(translate=translate)
    await message.answer(translate("name_game"), reply_markup=keyboard)
    await state.set_state(GameState.game_name)


@router.message(GameState.game_name)
async def game_name(
    message: Message, translate: LangType, state: FSMContext, db: AsyncSession
):
    new_game_db = Game(name=message.text.strip()) #type:ignore
    db.add(new_game_db)
    await db.commit()
    keyboard = await main_reply.admin_main(translate=translate)
    await message.answer(translate("new_game_created"), reply_markup=keyboard)
    await state.clear()


@router.message(TextIn(("Cancel", "Отмена", "Bekor qilish")))
async def cancel_game_creating(
    message: Message, translate: LangType, state: FSMContext
):
    keyboard = await main_reply.admin_main(translate=translate)
    current_state = await state.get_state()
    if current_state == 'AdminAdd:user_first_name':
        keyboard = await admin_op_reply.admin_btns(translate=translate)
    await message.answer(translate("game_cancelled"), reply_markup=keyboard)
    await state.clear()


@router.message(TextIn(("Games", "Игры", "O'yinlar")))
async def show_games(message: Message, translate: LangType):
    keyboard = await game_inline.games_message(translate=translate)
    await message.answer(translate("choose_completed"), reply_markup=keyboard)


@router.callback_query(F.data.startswith("games"))
async def get_games(query: CallbackQuery, translate: LangType, db: AsyncSession):
    is_completed = query.data.split(":")[1]  # type:ignore
    is_completed = False if is_completed == "False" else True
    page = 1
    logger.debug(page)

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
    response_txt: str = translate("not_found")
    count = 0
    game_id_list:list[list[int]]=[]
    for game in games:
        if count == 0:
            response_txt = ""
        count += 1
        response_txt += (
            f"<b>{game.id}</b>)<b>{translate('name')}</b>. {game.name}\n"
            f"<b>{translate('created_at')}</b>. {game.created_at.strftime('%m-%d-%Y')}\n"
            f"<b>{translate('end_time')}</b>. {game.updated_at.strftime('%m-%d-%Y')}\n\n"
        )
        game_id_list.append([count, game.id])
    keyboard = await game_inline.games_response(
        translate=translate,
        page=page,
        total_pages=total_pages,
        completed=is_completed,
        game_id_list=game_id_list,
    )
    await query.message.edit_text( #type:ignore
        text=response_txt, reply_markup=keyboard, parse_mode="HTML"
    )  # type:ignore


@router.callback_query(F.data.startswith("page"))
async def pagination_btns(query: CallbackQuery, translate: LangType, db: AsyncSession):
    data = query.data.split(":")  # type:ignore
    page = int(data[2])
    completed = data[1]
    completed = False if completed == "False" else True
    logger.debug(completed)
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
    response_txt = translate("not_found")
    count = 0
    game_id_list:list[list[int]]=[]
    for game in games:
        if count == 0:
            response_txt = ""
        count += 1
        response_txt += (
            f"<b>{count}</b>)<b>{translate('name')}</b>. {game.name}\n"
            f"<b>{translate('created_at')}</b>. {game.created_at.strftime('%m-%d-%Y')}\n"
            f"<b>{translate('end_time')}</b>. {game.updated_at.strftime('%m-%d-%Y')}\n\n"
        )
        game_id_list.append([count, game.id])
    keyboard = await game_inline.games_response(
        translate=translate,
        page=page,
        total_pages=total_pages,
        completed=completed,
        game_id_list=game_id_list,
    )
    await query.message.edit_text( #type:ignore
        text=response_txt, reply_markup=keyboard, parse_mode="HTML"
    )  # type:ignore


@router.callback_query(F.data.startswith("get_game"))
async def get_game_with_id(query: CallbackQuery, translate: LangType, db: AsyncSession):
    data = query.data.split(":") #type:ignore
    game_id = int(data[1])

    db_game = (
        (await db.execute(select(Game).where(Game.id == game_id)))
    ).scalars().first()
    if db_game is None:
        await query.message.answer(translate("not_found")) #type:ignore
        return
    response_txt = (
        f"<b>{translate('name')}</b>. {db_game.name}\n"
        f"<b>{translate('created_at')}</b>. {db_game.created_at.strftime('%m-%d-%Y')}\n"
        f"<b>{translate('end_time')}</b>. {db_game.updated_at.strftime('%m-%d-%Y')}\n\n"
    )
    await query.message.answer(response_txt, parse_mode='HTML') #type:ignore
