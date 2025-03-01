from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from telegram_bot.finit_states.calculate import CalculateFSM
from telegram_bot.funcs.calculate.calculate_actions import divide_odo
from telegram_bot.funcs.calculate.calculate_messages import calculate_ask_start_auto
from telegram_bot.funcs.menu import send_menu
from telegram_bot.keyboards.callbacks.car_select import CalculateCarChangeCallback

router = Router(name=__name__)


@router.message(StateFilter(CalculateFSM.result),
                F.text == "Готово")
async def h_calculate_result_menu(message: types.Message, state: FSMContext) -> None:
    await send_menu(message.from_user.id, state)


@router.message(StateFilter(CalculateFSM.result),
                F.text == "Разделить пробег на 2")
async def h_calculate_result_div2(message: types.Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    await message.reply(text=divide_odo(state_data.get("calc_full_odo"), 2))


@router.message(StateFilter(CalculateFSM.result),
                F.text == "Разделить пробег на 3")
async def h_calculate_result_div2(message: types.Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    await message.reply(text=divide_odo(state_data.get("calc_full_odo"), 3))


@router.message(StateFilter(CalculateFSM.result),
                F.text == "Разделить пробег на 4")
async def h_calculate_result_div2(message: types.Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    await message.reply(text=divide_odo(state_data.get("calc_full_odo"), 4))


@router.message(StateFilter(CalculateFSM.result),
                F.text == "Разделить пробег на 5")
async def h_calculate_result_div2(message: types.Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    await message.reply(text=divide_odo(state_data.get("calc_full_odo"), 5))


@router.callback_query(StateFilter(CalculateFSM.result),
                       CalculateCarChangeCallback.filter())
async def h_calculate_result_change_car(callback: CallbackQuery,
                                        state: FSMContext) -> None:
    await callback.message.delete()
    await calculate_ask_start_auto(callback.from_user.id, state)
