__all__ = ("router", )

from aiogram import Router
from .commands import router as router_commands
from .calculate import router as router_calculate
from .registration import router as router_registration


router = Router()
router.include_routers(router_commands, router_registration, router_calculate)
