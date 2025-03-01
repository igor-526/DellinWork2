from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def get_rm_by_str(keys: list[str]) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for key in keys:
        builder.button(text=key)
    builder.adjust(1)
    return builder.as_markup()
