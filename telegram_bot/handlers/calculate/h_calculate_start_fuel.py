from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from telegram_bot.finit_states.calculate import CalculateFSM
from telegram_bot.funcs.calculate.calculate_actions import calculate_set_start_fuel
from telegram_bot.funcs.calculate.calculate_messages import calculate_ask_refuel, calculate_ask_end_odo
from telegram_bot.funcs.menu import send_menu

router = Router(name=__name__)


@router.message(StateFilter(CalculateFSM.ask_start_fuel),
                F.text == "Подтвердить")
async def h_calculate_start_fuel_confirm(message: types.Message, state: FSMContext) -> None:
    await calculate_ask_refuel(message.from_user.id, state)


@router.message(StateFilter(CalculateFSM.ask_start_fuel),
                F.text == "Вернуться")
async def h_calculate_start_fuel_back(message: types.Message, state: FSMContext) -> None:
    await calculate_ask_end_odo(message.from_user.id, state)


@router.message(StateFilter(CalculateFSM.ask_start_fuel),
                F.text == "Отмена")
async def h_calculate_start_fuel_cancel(message: types.Message, state: FSMContext) -> None:
    await send_menu(message.from_user.id, state)


@router.message(StateFilter(CalculateFSM.ask_start_fuel))
async def h_calculate_start_fuel_input(message: types.Message, state: FSMContext) -> None:
    await calculate_set_start_fuel(message, state)
