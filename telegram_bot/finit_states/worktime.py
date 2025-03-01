from aiogram.fsm.state import StatesGroup, State


class WorkTimeFSM(StatesGroup):
    ask_start_time = State()
    ask_end_time = State()
    ask_day_type = State()
