__all__ = ("router", )

from aiogram import Router
from .h_reg_service_number import router as router_h_reg_service_number
from .h_reg_name import router as router_h_reg_name
from .h_reg_city_base import router as router_h_reg_city_base

router = Router()
router.include_routers(router_h_reg_service_number,
                       router_h_reg_name,
                       router_h_reg_city_base)
