from aiogram.fsm.state import StatesGroup, State


class RegistrationFSM(StatesGroup):
    ask_service_number = State()
    ask_name = State()
    ask_name_change = State()
    ask_city = State()
    ask_base = State()
