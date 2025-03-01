__all__ = ("router", )

from aiogram import Router
from .h_calculate_start_odo import router as router_h_calculate_start_odo
from .h_calculate_end_odo import router as router_h_calculate_end_odo
from .h_calculate_start_fuel import router as router_h_calculate_start_fuel
from .h_calculate_refuel import router as router_h_calculate_refuel
from .h_calculate_car import router as router_h_calculate_car
from .h_calculate_result import router as router_h_calculate_result

router = Router()
router.include_routers(router_h_calculate_start_odo,
                       router_h_calculate_end_odo,
                       router_h_calculate_start_fuel,
                       router_h_calculate_refuel,
                       router_h_calculate_car,
                       router_h_calculate_result)
