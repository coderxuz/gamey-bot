from aiogram import Router

from . import command, game, admin_operation
from bot.app.filters.auth import Registered

router = Router()
router.message.filter(Registered(is_admin=True))

router.include_router(command.router)
router.include_router(game.router)
router.include_router(admin_operation.router)
