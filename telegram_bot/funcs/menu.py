from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from profile_management.models import NewUser
from telegram_bot.create_bot import bot


async def send_menu(tg_id: int, state: FSMContext, custom_text: str = "Выберите действие"):
    user_groups = [group.name async for group in (await NewUser.objects.aget(telegram_id=tg_id)).groups.all()]
    keys = []
    if "MKTDriver" in user_groups:
        keys.append([KeyboardButton(text="Расчёт путевого листа")])
        keys.append([KeyboardButton(text="Добавить рабочее время")])
        keys.append([KeyboardButton(text="Контакты")])
        keys.append([KeyboardButton(text="Ближайшая шинка/мойка")])
    keys.append([KeyboardButton(text="Настройки"), KeyboardButton(text="Отчёты")])
    await bot.send_message(chat_id=tg_id,
                           text=custom_text,
                           reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keys))
    await state.clear()
