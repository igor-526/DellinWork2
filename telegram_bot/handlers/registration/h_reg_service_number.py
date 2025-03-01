from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from telegram_bot.finit_states.registration import RegistrationFSM
from telegram_bot.funcs.registration.registration import (f_registration_set_service_number)

router = Router(name=__name__)


@router.message(StateFilter(RegistrationFSM.ask_service_number))
async def h_registration_service_number_asked(message: types.Message, state: FSMContext) -> None:
    await f_registration_set_service_number(message, state)
