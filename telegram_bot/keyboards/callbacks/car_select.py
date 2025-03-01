from aiogram.filters.callback_data import CallbackData


class CalculateCarSelectCallback(CallbackData, prefix="calculate_car"):
    id: int


class CalculateCarChangeCallback(CallbackData, prefix="calculate_car_change"):
    id: int

