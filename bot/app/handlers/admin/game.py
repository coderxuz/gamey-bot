from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from aiogram.filters import CommandStart, CommandObject
from sqlalchemy import func

from bot.app.filters.text_int import TextIn
from bot.app.middlewares.translations import LangType
from database.models import Game, User,UserGame
from bot.app.keyboards.admin.game import inline as game_inline
from bot.app.keyboards.admin.game import reply as game_reply
from bot.app.keyboards.main import reply as main_reply
from bot.app.keyboards.admin.admin_operation import reply as admin_op_reply
from bot.app.states.game import GameState
from common import logger, ADMIN_ID, BOT_USERNAME
from bot.app.filters.command_args import CommandFilter
from bot.app.services.hash_id import encode_id, decode_id
from bot.app.middlewares.translations import TranslationMiddleware
from bot import bot



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
    new_game_db = Game(name=message.text.strip())  # type:ignore
    db.add(new_game_db)
    await db.commit()
    keyboard = await main_reply.admin_main(translate=translate)
    if message.from_user.id == ADMIN_ID: #type:ignore
        keyboard = await main_reply.admin_main(translate=translate, main_admin=True)
    await message.answer(translate("new_game_created"), reply_markup=keyboard)
    await state.clear()


@router.message(TextIn(("Cancel", "Отмена", "Bekor qilish")))
async def cancel_game_creating(
    message: Message, translate: LangType, state: FSMContext
):
    keyboard = await main_reply.admin_main(translate=translate)
    current_state = await state.get_state()
    if current_state == "AdminAdd:user_first_name":
        keyboard = await admin_op_reply.admin_btns(translate=translate)
    if message.from_user.id == ADMIN_ID:
        keyboard = await main_reply.admin_main(translate=translate, main_admin=True)
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
    game_id_list: list[list[int]] = []
    for game in games:
        if count == 0:
            response_txt = ""
        count += 1
        player_count = (await db.execute(select(func.count(UserGame.user_tg_id)).where(UserGame.game_id==game.id))).scalar() or 0
        response_txt += (
            f"<b>{count}</b>)<b>{translate('name')}</b>. {game.name}\n"
            f"<b>{translate('created_at')}</b>. {game.created_at.strftime('%m-%d-%Y')}\n"
            f"<b>{translate('players')}</b>. {player_count}\n"
            f"<b>{translate('status')}</b>. {translate("end") if game.is_completed else translate("not_end")}\n\n"
        )
        game_id_list.append([count, game.id])
    keyboard = await game_inline.games_response(
        translate=translate,
        page=page,
        total_pages=total_pages,
        completed=is_completed,
        game_id_list=game_id_list,
    )
    await query.message.edit_text(  # type:ignore
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
    game_id_list: list[list[int]] = []
    for game in games:
        if count == 0:
            response_txt = ""
        count += 1
        player_count = (await db.execute(select(func.count(UserGame.user_tg_id)).where(UserGame.game_id==game.id))).scalar() or 0
        response_txt += (
            f"<b>{count}</b>)<b>{translate('name')}</b>. {game.name}\n"
            f"<b>{translate('created_at')}</b>. {game.created_at.strftime('%m-%d-%Y')}\n"
            f"<b>{translate('players')}</b>. {player_count}\n"
            f"<b>{translate('status')}</b>. {translate("end") if game.is_completed else translate("not_end")}\n\n"
        )
        game_id_list.append([count, game.id])
    keyboard = await game_inline.games_response(
        translate=translate,
        page=page,
        total_pages=total_pages,
        completed=completed,
        game_id_list=game_id_list,
    )
    await query.message.edit_text(  # type:ignore
        text=response_txt, reply_markup=keyboard, parse_mode="HTML"
    )  # type:ignore


@router.callback_query(F.data.startswith("get_game"))
async def get_game_with_id(query: CallbackQuery, translate: LangType, db: AsyncSession):
    data = query.data.split(":")  # type:ignore
    game_id = int(data[1])

    db_game = (
        ((await db.execute(select(Game).where(Game.id == game_id)))).scalars().first()
    )
    if db_game is None:
        await query.message.answer(translate("not_found"))  # type:ignore
        return
    player_count = (await db.execute(select(func.count(UserGame.user_tg_id)).where(UserGame.game_id==game_id))).scalar() or 0
    
    response_txt = (
        f"<b>{translate('name')}</b>. {db_game.name}\n"
        f"<b>{translate('created_at')}</b>. {db_game.created_at.strftime('%m-%d-%Y')}\n"
        f"<b>{translate('players')}</b>. {player_count}\n"
        f"<b>{translate('status')}</b>. {translate("end") if db_game.is_completed else translate("not_end")}\n\n"
    )
    keyboard = await game_inline.single_game(translate=translate, game_id=db_game.id)
    await query.message.answer(
        response_txt, parse_mode="HTML", reply_markup=keyboard
    )  # type:ignore


@router.callback_query(F.data.startswith("add_user"))
async def add_player(query: CallbackQuery, translate: LangType, db: AsyncSession):
    data = query.data.split(":")  # type:ignore
    game_id = int(data[1])

    db_game = (
        ((await db.execute(select(Game).where(Game.id == game_id)))).scalars().first()
    )
    if db_game is None:
        await query.message.answer(translate("not_found"))  # type:ignore
        return
    encrypted_game_id = encode_id(db_game.id)
    game_link = f"https://t.me/{BOT_USERNAME}?start=game_{encrypted_game_id}"
    await query.message.answer(
        f"{translate('send_link')}\n{translate("link")}: <code>{game_link}</code>",
        parse_mode="HTML",
    )


@router.message(CommandStart(), CommandFilter("game_"))
async def join_game1(
    message: Message, command: CommandObject, translate: LangType, db: AsyncSession
):
    command_args=None
    if command.args:
        command_args = command.args.split("_")
    game_code = command_args[1] if command_args and len(command_args) == 2 else None
    if not game_code:
        return
    logger.debug(game_code)
    try:
        game_id = decode_id(game_code)
        db_game = (
            (await db.execute(select(Game).where(Game.id == game_id))).scalars().first()
        )
        if not db_game:
            await message.answer(translate("not_found"))
            return
        player_count = (await db.execute(select(func.count(UserGame.user_tg_id)).where(UserGame.game_id==game_id))).scalar() or 0
        response_txt = (
            f"<b>{translate('name')}</b>. {db_game.name}\n"
            f"<b>{translate('created_at')}</b>. {db_game.created_at.strftime('%m-%d-%Y')}\n"
            f"<b>{translate('players')}</b>. {player_count}\n"
            f"<b>{translate('status')}</b>. {translate("end") if db_game.is_completed else translate("not_end")}\n\n"
            f"<b>{translate("do_you_want_join")}</b>"
        )
        keyboard = await game_inline.join_game(translate=translate, game_id=game_id)
        await message.answer(response_txt, parse_mode="HTML", reply_markup=keyboard)
    except Exception as e:
        #raise e
        logger.error(str(e))
        await message.answer(translate("not_found"))
        return


@router.callback_query(F.data.startswith("join_game"))
async def join_player(query: CallbackQuery, translate: LangType, db: AsyncSession):
    data = query.data.split(":")
    game_id = data[1] if len(data) > 1 else None
    if not game_id:
        await query.message.delete()
        return
    game_id = int(game_id)
    db_game = (
        (
            await db.execute(
                select(Game).where(Game.id == game_id, Game.is_completed == False)
            )
        )
        .scalars()
        .first()
    )
    db_user = (
        (await db.execute(select(User).where(User.tg_id == query.from_user.id)))
        .scalars()
        .first()
    )
    if not db_game or not db_user:
        await query.message.delete()
        await query.message.answer(translate("not_found"))
        return
    user_lang = await TranslationMiddleware.get_user_language(
        user_id=query.from_user.id
    )
    logger.debug(user_lang)
    response_txt = (
        f"{translate("do_you_want_join_user",user_lang)}\n\n"  # type:ignore
        f"{translate("first_name_txt",user_lang)} - <b>{db_user.first_name}</b>\n"  # type:ignore
        f"{translate("last_name_txt", user_lang)} - <b>{db_user.last_name}</b>\n"  # type:ignore
        f"{translate("phone_number", user_lang)} <b>{db_user.phone}</b>\n\n"  # type:ignore
        f"{translate("name_game_txt", user_lang)} - <b>{db_game.name}</b>\n"  # type:ignore
        f"{translate('created_at',user_lang)} - <b>{db_game.created_at.strftime('%m-%d-%Y')}</b>\n"  # type:ignore
    )
    admins = (
        (await db.execute(select(User).where(User.is_admin == True))).scalars().all()
    )
    keyboard = await game_inline.add_game(
        translate=translate, user_lang=user_lang, game_id=game_id, user_id=db_user.tg_id
    )
    for admin in admins:
        await bot.send_message(
            chat_id=admin.tg_id,
            text=response_txt,
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    await query.message.answer(text=translate("request_sent"))
    await query.message.delete()


@router.callback_query(F.data.startswith("add_game"))
async def add_player1(query: CallbackQuery, translate: LangType, db: AsyncSession):
    data = query.data.split(":")
    logger.debug(data)
    _,game_id, user_tg_id = data if len(data) == 3 else None
    if not game_id:
        await query.message.delete()
        return
    game_id = int(game_id)
    user_tg_id = int(user_tg_id)
    db_game = (
        (
            await db.execute(
                select(Game).where(Game.id == game_id, Game.is_completed == False)
            )
        )
        .scalars()
        .first()
    )
    db_user = (
        (await db.execute(select(User).where(User.tg_id ==user_tg_id)))
        .scalars()
        .first()
    )
    if not db_game or not db_user:
        await query.message.delete()
        await query.message.answer(translate("not_found"))
        return
    new_relation = UserGame(
        user_tg_id= user_tg_id,
        game_id = game_id
    )
    db.add(new_relation)
    await db.commit()
    await query.message.answer(translate("user_added_game"))