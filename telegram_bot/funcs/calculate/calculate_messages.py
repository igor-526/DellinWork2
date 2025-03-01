from aiogram import types
from aiogram.fsm.context import FSMContext
from autos.models import Car
from profile_management.models import NewUser
from telegram_bot.create_bot import bot
from telegram_bot.finit_states.calculate import CalculateFSM
from telegram_bot.keyboards.calculate import get_autos_buttons
from telegram_bot.keyboards.easy_keyboards import get_rm_by_str


async def calculate_start_message(message: types.Message, state: FSMContext):
    user = await NewUser.objects.aget(telegram_id=message.from_user.id)
    await state.update_data(calc_start_odo=user.settings_last_odo,
                            calc_start_fuel=user.settings_last_fuel,
                            calc_start_auto=user.setting_last_auto.id if user.setting_last_auto else None)
    await message.answer(text="Функция позволяет безошибочно выполнить расчёт путевого листа")
    await calculate_ask_start_odo(message.from_user.id, state)


async def calculate_ask_start_odo(tg_id: int, state: FSMContext):
    state_data = await state.get_data()
    start_odo = state_data.get('calc_start_odo')
    if start_odo:
        text = (f'Ваш начальный пробег: {start_odo}\n'
                f'Если это не так, введите корректный начальный пробег')
        rm = get_rm_by_str(["Подтвердить", "Отмена"])
    else:
        text = 'Пожалуйста, введите начальный пробег'
        rm = get_rm_by_str(["Отмена"])
    await bot.send_message(chat_id=tg_id,
                           text=text,
                           reply_markup=rm)
    await state.set_state(CalculateFSM.ask_start_odo)


async def calculate_ask_end_odo(tg_id: int, state: FSMContext):
    state_data = await state.get_data()
    end_odo = state_data.get('calc_end_odo')
    if end_odo:
        text = (f'Ваш конечный пробег: {end_odo}\n'
                f'Если это не так, введите корректный конечный пробег')
        rm = get_rm_by_str(["Подтвердить", "Вернуться", "Отмена"])
    else:
        text = 'Пожалуйста, введите конечный пробег'
        rm = get_rm_by_str(["Вернуться", "Отмена"])
    await bot.send_message(chat_id=tg_id,
                           text=text,
                           reply_markup=rm)
    await state.set_state(CalculateFSM.ask_end_odo)


async def calculate_ask_start_fuel(tg_id: int, state: FSMContext):
    state_data = await state.get_data()
    start_fuel = state_data.get('calc_start_fuel')
    if start_fuel:
        text = (f'Ваш начальный остаток топлива: {start_fuel}\n'
                f'Если это не так, введите корректный начальный остаток топлива')
        rm = get_rm_by_str(["Подтвердить", "Вернуться", "Отмена"])
    else:
        text = 'Пожалуйста, введите начальный остаток топлива'
        rm = get_rm_by_str(["Вернуться", "Отмена"])
    await bot.send_message(chat_id=tg_id,
                           text=text,
                           reply_markup=rm)
    await state.set_state(CalculateFSM.ask_start_fuel)


async def calculate_ask_refuel(tg_id: int, state: FSMContext):
    state_data = await state.get_data()
    refuel = state_data.get('calc_refuel')
    if refuel:
        text = (f'Ваша заправка составила {refuel}л.\n'
                f'Если это не так, введите корректную заправку')
        rm = get_rm_by_str(["Не заправлялся", "Вернуться", "Отмена"])
    else:
        text = ('Вы заправлялись? Если да, введите количество заправленных литров '
                'в одном из следующих форматов:\n'
                'X\n'
                'X.X\n'
                'X,X')
        rm = get_rm_by_str(["Не заправлялся", "Вернуться", "Отмена"])
    await bot.send_message(chat_id=tg_id,
                           text=text,
                           reply_markup=rm)
    await state.set_state(CalculateFSM.ask_refuel)


async def calculate_ask_start_auto(tg_id: int, state: FSMContext):
    car_list = [{"id": car.id,
                 "name": car.name} async for car in Car.objects.filter(base__newuser__telegram_id=tg_id)]
    await bot.send_message(chat_id=tg_id,
                           text="Пожалуйста, выберите автомобиль из списка",
                           reply_markup=get_rm_by_str(["Вернуться", "Отмена"]))
    await bot.send_message(chat_id=tg_id,
                           text="Автомобили",
                           reply_markup=get_autos_buttons(car_list))
    await state.set_state(CalculateFSM.ask_car)

