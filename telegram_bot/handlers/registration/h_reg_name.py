from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from telegram_bot.finit_states.registration import RegistrationFSM
from telegram_bot.funcs.registration.registration import (f_registration_ask_service_number,
                                                          f_registration_ask_name, f_registration_change_name,
                                                          f_registration_set_name)
from telegram_bot.keyboards.easy_keyboards import get_rm_by_str

router = Router(name=__name__)


@router.message(StateFilter(RegistrationFSM.ask_name),
                F.text == "Подтвердить")
async def h_registration_name_asked_confirm(message: types.Message, state: FSMContext) -> None:
    await f_registration_set_name(message, state)


@router.message(StateFilter(RegistrationFSM.ask_name),
                F.text == "Изменить")
async def h_registration_name_asked_change(message: types.Message, state: FSMContext) -> None:
    await message.answer(text="Пожалуйста, введите через пробел сначала Вашу фамилию, затем имя\n"
                              "Например, Иванов Иван",
                         reply_markup=get_rm_by_str(['Отмена']))
    await state.set_state(RegistrationFSM.ask_name_change)


@router.message(StateFilter(RegistrationFSM.ask_name),
                F.text == "Вернуться к табельному номеру")
async def h_registration_name_asked_back(message: types.Message, state: FSMContext) -> None:
    await f_registration_ask_service_number(message.from_user.id, state)


@router.message(StateFilter(RegistrationFSM.ask_name))
async def h_registration_name_asked_invalid(message: types.Message, state: FSMContext) -> None:
    await message.answer(text="Я вас не понял :(\nПожалуйста, выберите действие на клавиатуре снизу",
                         reply_markup=get_rm_by_str([
                             "Подтвердить",
                             "Изменить",
                             "Вернуться к табельному номеру"
                         ]))


@router.message(StateFilter(RegistrationFSM.ask_name_change),
                F.text == "Отмена")
async def h_registration_name_asked_change_cancel(message: types.Message, state: FSMContext) -> None:
    await f_registration_ask_name(message, state)


@router.message(StateFilter(RegistrationFSM.ask_name_change))
async def h_registration_name_asked_change_input(message: types.Message, state: FSMContext) -> None:
    await f_registration_change_name(message, state)
