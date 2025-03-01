from aiogram.filters.callback_data import CallbackData


class RegistrationCityCallback(CallbackData, prefix="reg_city"):
    id: int


class RegistrationBaseCallback(CallbackData, prefix="reg_base"):
    id: int
