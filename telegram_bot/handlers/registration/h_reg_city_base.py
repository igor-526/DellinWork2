from aiogram import types, Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from telegram_bot.create_bot import bot
from telegram_bot.finit_states.registration import RegistrationFSM
from telegram_bot.funcs.registration.registration import f_registration_ask_name, f_registration_ask_city, \
    f_registration_ask_base, f_registration_add_user
from telegram_bot.keyboards.callbacks.registartion import RegistrationCityCallback, RegistrationBaseCallback
from telegram_bot.keyboards.easy_keyboards import get_rm_by_str

router = Router(name=__name__)


@router.message(StateFilter(RegistrationFSM.ask_city),
                F.text == "Вернуться к имени")
async def h_reg_city_back(message: types.Message, state: FSMContext) -> None:
    await f_registration_ask_name(message, state)


@router.message(StateFilter(RegistrationFSM.ask_base),
                F.text == "Вернуться к городу")
async def h_reg_base_back(message: types.Message, state: FSMContext) -> None:
    await f_registration_ask_city(message.from_user.id, state)


@router.callback_query(StateFilter(RegistrationFSM.ask_city),
                       RegistrationCityCallback.filter())
async def h_reg_city(callback: CallbackQuery,
                     callback_data: RegistrationCityCallback,
                     state: FSMContext) -> None:
    await state.update_data(reg_city=callback_data.id)
    await bot.send_message(chat_id=callback.from_user.id,
                           text="Отлично! Осталось немного",
                           reply_markup=get_rm_by_str(['Вернуться к городу']))
    await callback.message.delete()
    await f_registration_ask_base(callback.from_user.id, state)


@router.callback_query(StateFilter(RegistrationFSM.ask_base),
                       RegistrationBaseCallback.filter())
async def h_reg_base(callback: CallbackQuery,
                     callback_data: RegistrationBaseCallback,
                     state: FSMContext) -> None:
    await state.update_data(reg_base=callback_data.id)
    await callback.message.delete()
    await f_registration_add_user(callback.from_user.id, state)