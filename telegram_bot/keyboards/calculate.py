from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from telegram_bot.keyboards.callbacks.car_select import CalculateCarSelectCallback, CalculateCarChangeCallback


def get_autos_buttons(autos: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for auto in autos:
        builder.button(
            text=auto['name'],
            callback_data=CalculateCarSelectCallback(id=auto['id'])
        )
    builder.adjust(1)
    return builder.as_markup()


def get_change_auto_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Изменить ТС",
        callback_data=CalculateCarChangeCallback(id=0)
    )
    builder.adjust(1)
    return builder.as_markup()