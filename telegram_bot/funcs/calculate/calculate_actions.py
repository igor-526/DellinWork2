from aiogram import types
from aiogram.fsm.context import FSMContext
from autos.models import Car
from consumption.models import Consumption
from profile_management.models import NewUser
from telegram_bot.create_bot import bot
from telegram_bot.finit_states.calculate import CalculateFSM
from telegram_bot.funcs.calculate.calculate_messages import calculate_ask_end_odo, calculate_ask_start_fuel, \
    calculate_ask_refuel, calculate_ask_start_auto
from telegram_bot.keyboards.calculate import get_change_auto_button
from telegram_bot.keyboards.easy_keyboards import get_rm_by_str


async def calculate_set_start_odo(message: types.Message, state: FSMContext):
    try:
        start_odo = int(message.text)
        if start_odo < 0:
            await message.reply(text="Так не получилось :(\n"
                                     "Начальный пробег не может быть отрицательным")
            return
        await state.update_data(calc_start_odo=start_odo)
        await calculate_ask_end_odo(message.from_user.id, state)
    except ValueError:
        await message.reply(text="Так не получилось :(\n"
                                 "Пожалуйста, введите начальный пробег используя только цифры\n"
                                 "Например, 114689")


async def calculate_set_end_odo(message: types.Message, state: FSMContext):
    try:
        end_odo = int(message.text)
        if end_odo < 0:
            await message.reply(text="Так не получилось :(\n"
                                     "Конечный пробег не может быть отрицательным")
            return
        state_data = await state.get_data()
        start_odo = state_data.get("calc_start_odo")
        if end_odo < start_odo:
            await message.reply(text="Так не получилось :(\n"
                                     "Конечный пробег не может быть меньше начального")
            return
        await state.update_data(calc_end_odo=end_odo)
        await calculate_ask_start_fuel(message.from_user.id, state)
    except ValueError:
        await message.reply(text="Так не получилось :(\n"
                                 "Пожалуйста, введите конечный пробег используя только цифры\n"
                                 "Например, 114754")


async def calculate_set_start_fuel(message: types.Message, state: FSMContext):
    try:
        start_fuel = int(message.text)
        if start_fuel < 1:
            await message.reply(text="Так не получилось :(\n"
                                     "Начальный остаток топлива не может быть менее 1 литра")
            return
        await state.update_data(calc_start_fuel=start_fuel)
        await calculate_ask_refuel(message.from_user.id, state)
    except ValueError:
        await message.reply(text="Так не получилось :(\n"
                                 "Пожалуйста, введите начальный остаток топлива используя только цифры\n"
                                 "Например, 36")


async def calculate_set_refuel(message: types.Message, state: FSMContext, null: bool = False):
    state_data = await state.get_data()
    if null:
        await state.update_data(calc_refuel=0)
        if state_data.get("calc_start_auto") is None:
            await calculate_ask_start_auto(message.from_user.id, state)
        else:
            await calculate_all(message.from_user.id, state)
        return
    try:
        refuel = float(message.text.replace(",", "."))
        if refuel < 0:
            await message.reply(text="Так не получилось :(\n"
                                     "Количество заправленных литров не может быть отрицательным")
            return
        await state.update_data(calc_refuel=refuel)
        if state_data.get("calc_start_auto") is None:
            await calculate_ask_start_auto(message.from_user.id, state)
        else:
            await calculate_all(message.from_user.id, state)
    except ValueError:
        await message.reply(text=('Так не получилось :(\n'
                                  'Пожалуйста, введите количество заправленных литров '
                                  'в одном из следующих форматов:\n'
                                  'X\n'
                                  'X.X\n'
                                  'X,X\n'
                                  'Например, 54.21'))


async def calculate_all(tg_id: int, state: FSMContext):
    async def create_note():
        note = await Consumption.objects.acreate(
            driver=user,
            consumption=all_consumption,
            odo=full_odo,
            econ=fuel_econ,
            burnout=fuel_burnout,
            car=car
        )
        return note.id

    async def change_note():
        note = await Consumption.objects.aget(pk=state_data.get("calc_note_id"))
        note.driver = user
        note.consumption = all_consumption
        note.odo = full_odo
        note.econ = fuel_econ
        note.burnout = fuel_burnout
        note.car = car
        await note.asave()

    state_data = await state.get_data()
    user = await NewUser.objects.select_related("base", "base__city").aget(telegram_id=tg_id)
    car = await Car.objects.aget(pk=state_data.get("calc_start_auto"))
    full_odo = state_data.get("calc_end_odo") - state_data.get("calc_start_odo")
    await state.update_data(calc_full_odo=full_odo)
    consumption = car.consumption_winter if user.base.city.consumption_time \
        else car.consumption_summer
    all_consumption = full_odo/100 * consumption
    fuel_econ = 0
    fuel_burnout = 0
    end_fuel = state_data.get("calc_start_fuel") + state_data.get("calc_refuel") - all_consumption
    if end_fuel < 1:
        fuel_econ = (1 - end_fuel)
        end_fuel = 1
    if end_fuel > car.tank:
        fuel_burnout = end_fuel - car.tank
        end_fuel = car.tank
    await bot.send_message(chat_id=tg_id,
                           text=f'Ваше ТС: {car.name}\n'
                                f'Ёмкость бака: {car.tank} л.\n'
                                f'Расход: {consumption} л./100км'
                                f'({"ЗИМНИЙ" if user.base.city.consumption_time else "ЛЕТНИЙ"})',
                           reply_markup=get_change_auto_button())
    text = (f'Пробег за рейс: {full_odo}км\n'
            f'Остаток в баке: {end_fuel}')
    if fuel_econ:
        text += f'\nЭкономия: {fuel_econ}\n'
    if fuel_burnout:
        text += f'\nПережог: {fuel_burnout}\n'
    await bot.send_message(chat_id=tg_id,
                           text=text,
                           reply_markup=get_rm_by_str(["Готово",
                                                       "Разделить пробег на 2",
                                                       "Разделить пробег на 3",
                                                       "Разделить пробег на 4",
                                                       "Разделить пробег на 5"]))
    if state_data.get("calc_note_id") is None:
        await state.update_data(calc_note_id=await create_note())
    else:
        await change_note()
    await state.set_state(CalculateFSM.result)


def divide_odo(km: int, count: int) -> str:
    text = ""
    full = km // count
    x = km % count
    for i in range(0, count):
        if i == 0:
            text += f"{full + x} км"
        else:
            text += f'\n{full} км'
    return text


