from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram_bot.keyboards.callbacks.registartion import RegistrationCityCallback, RegistrationBaseCallback


def get_city_buttons(cities: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for city in cities:
        builder.button(
            text=city['name'],
            callback_data=RegistrationCityCallback(id=city['id'])
        )
    builder.adjust(1)
    return builder.as_markup()


def get_bases_buttons(bases: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for base in bases:
        builder.button(
            text=base['name'],
            callback_data=RegistrationBaseCallback(id=base['id'])
        )
    builder.adjust(1)
    return builder.as_markup()
