__all__ = ("router", )

from aiogram import Router
from .menu import router as router_menu

router = Router()
router.include_routers(router_menu)
