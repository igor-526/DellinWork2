from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from telegram_bot.finit_states.calculate import CalculateFSM
from telegram_bot.funcs.calculate.calculate_actions import calculate_all
from telegram_bot.funcs.calculate.calculate_messages import calculate_ask_refuel
from telegram_bot.funcs.menu import send_menu
from telegram_bot.keyboards.callbacks.car_select import CalculateCarSelectCallback

router = Router(name=__name__)


@router.message(StateFilter(CalculateFSM.ask_car),
                F.text == "Отмена")
async def h_calculate_car_select_cancel(message: types.Message, state: FSMContext) -> None:
    await send_menu(message.from_user.id, state)


@router.message(StateFilter(CalculateFSM.ask_car),
                F.text == "Вернуться")
async def h_calculate_car_select_back(message: types.Message, state: FSMContext) -> None:
    await calculate_ask_refuel(message.from_user.id, state)


@router.callback_query(StateFilter(CalculateFSM.ask_car),
                       CalculateCarSelectCallback.filter())
async def h_calculate_car_select_input(callback: CallbackQuery,
                                       callback_data: CalculateCarSelectCallback,
                                       state: FSMContext) -> None:
    await state.update_data(calc_start_auto=callback_data.id)
    await callback.message.delete()
    await calculate_all(callback.from_user.id, state)
