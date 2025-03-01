from aiogram.fsm.state import StatesGroup, State


class CalculateFSM(StatesGroup):
    ask_start_odo = State()
    ask_end_odo = State()
    ask_start_fuel = State()
    ask_refuel = State()
    ask_car = State()
    result = State()
