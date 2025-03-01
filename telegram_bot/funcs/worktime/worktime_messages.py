import datetime
from aiogram import types
from aiogram.fsm.context import FSMContext
from telegram_bot.create_bot import bot
from telegram_bot.finit_states.worktime import WorkTimeFSM
from telegram_bot.keyboards.easy_keyboards import get_rm_by_str


async def worktime_ask_start_time(tg_id: int, state: FSMContext):
    now = datetime.datetime.now()
    now = {
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "hour": now.hour,
        "minute": now.minute,
        "second": 0
    }
    await state.update_data(wt_end=now)
    await bot.send_message(chat_id=tg_id,
                           text="Введите время начала рабочего дня по путевому листу в одном из следующих форматов:\n"
                                "ЧЧ:ММ\n"
                                "ЧЧ.ММ\n"
                                "ЧЧ ММ",
                           reply_markup=get_rm_by_str(["Отмена"]))
    await state.set_state(WorkTimeFSM.ask_start_time)
