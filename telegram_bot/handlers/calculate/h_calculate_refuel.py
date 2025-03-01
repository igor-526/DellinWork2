from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from telegram_bot.finit_states.calculate import CalculateFSM
from telegram_bot.funcs.calculate.calculate_actions import calculate_set_refuel
from telegram_bot.funcs.calculate.calculate_messages import calculate_ask_start_fuel
from telegram_bot.funcs.menu import send_menu

router = Router(name=__name__)


@router.message(StateFilter(CalculateFSM.ask_refuel),
                F.text == "Не заправлялся")
async def h_calculate_refuels_null(message: types.Message, state: FSMContext) -> None:
    await calculate_set_refuel(message, state, True)


@router.message(StateFilter(CalculateFSM.ask_refuel),
                F.text == "Вернуться")
async def h_calculate_refuels_back(message: types.Message, state: FSMContext) -> None:
    await calculate_ask_start_fuel(message.from_user.id, state)


@router.message(StateFilter(CalculateFSM.ask_refuel),
                F.text == "Отмена")
async def h_calculate_refuels_cancel(message: types.Message, state: FSMContext) -> None:
    await send_menu(message.from_user.id, state)


@router.message(StateFilter(CalculateFSM.ask_refuel))
async def h_calculate_refuels_input(message: types.Message, state: FSMContext) -> None:
    await calculate_set_refuel(message, state)
