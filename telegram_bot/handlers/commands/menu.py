from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from telegram_bot.funcs.calculate.calculate_messages import calculate_start_message
from telegram_bot.funcs.menu import send_menu

router = Router(name=__name__)


@router.message(Command('reset'))
async def h_menu_reset(message: types.Message, state: FSMContext):
    await message.answer("Сброс выполнен")
    await state.clear()


@router.message(StateFilter(None),
                F.text == "Расчёт путевого листа")
async def h_menu_calculate(message: types.Message, state: FSMContext) -> None:
    await calculate_start_message(message, state)


@router.message(StateFilter(None),
                F.text == "Добавить рабочее время")
async def h_menu_worktime(message: types.Message, state: FSMContext) -> None:
    await message.answer("Функция находится в разработке")


@router.message(StateFilter(None),
                F.text == "Контакты")
async def h_menu_contacts(message: types.Message, state: FSMContext) -> None:
    await message.answer("Функция находится в разработке")


@router.message(StateFilter(None),
                F.text == "Ближайшая шинка/мойка")
async def h_menu_wash_repair(message: types.Message, state: FSMContext) -> None:
    await message.answer("Функция находится в разработке")


@router.message(StateFilter(None),
                F.text == "Настройки")
async def h_menu_settings(message: types.Message, state: FSMContext) -> None:
    await message.answer("Функция находится в разработке")


@router.message(StateFilter(None),
                F.text == "Отчёты")
async def h_menu_reports(message: types.Message, state: FSMContext) -> None:
    await message.answer("Функция находится в разработке")


@router.message(StateFilter(None))
async def h_menu_error(message: types.Message, state: FSMContext) -> None:
    await send_menu(message.from_user.id, state,
                    "Я Вас не понял :(\nПожалуйста, выберите действие из меню")
