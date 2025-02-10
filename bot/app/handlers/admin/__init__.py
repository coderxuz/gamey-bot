
from aiogram import Router

from . import command, game

router = Router()
router.include_router(command.router)
router.include_router(game.router)
