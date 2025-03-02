from aiogram import types
from aiogram.fsm.context import FSMContext
from django.contrib.auth.models import Group
from profile_management.utils import get_random_password
from telegram_bot.create_bot import bot
from telegram_bot.finit_states.registration import RegistrationFSM
from telegram_bot.funcs.menu import send_menu
from telegram_bot.keyboards.easy_keyboards import get_rm_by_str
from bases.models import City, Base
from telegram_bot.keyboards.registration import get_city_buttons, get_bases_buttons
from profile_management.models import NewUser
from django.contrib.auth.hashers import make_password


async def f_registration_start(tg_id: int, state: FSMContext):
    await bot.send_message(chat_id=tg_id,
                           text="Добро пожаловать в бот! Давайте приступим к регистрации!")
    await f_registration_ask_service_number(tg_id, state)


async def f_registration_ask_service_number(tg_id: int, state: FSMContext):
    state_data = await state.get_data()
    if state_data.get("reg_service_number"):
        text = (f"Ваш табельный номер: {state_data.get('reg_service_number')}\n"
                f"Верно? Введите верный табельный номер, если нет или нажмите кнопку 'Подтвердить'")
        rm = get_rm_by_str(["Подтвердить"])
    else:
        text = "Введите, пожалуйста, Ваш табельный номер"
        rm = None
    await bot.send_message(chat_id=tg_id,
                           text=text,
                           reply_markup=rm)
    await state.set_state(RegistrationFSM.ask_service_number)


async def f_registration_set_service_number(message: types.Message, state: FSMContext):
    if message.text == "Подтвердить":
        await message.answer("Отлично! Перейдём к следующему шагу")
        await f_registration_ask_name(message, state)
        return
    try:
        await state.update_data(reg_service_number=int(message.text))
        await message.answer("Отлично! Перейдём к следующему шагу")
        await f_registration_ask_name(message, state)
    except ValueError:
        await message.answer("Не получилось. Пожалуйста, введите Ваш табельный номер. Используйте только цифры")


async def f_registration_ask_name(message: types.Message, state: FSMContext):
    state_data = await state.get_data()

    first_name = state_data.get("reg_first_name") if state_data.get("reg_first_name") else message.from_user.first_name
    last_name = state_data.get("reg_last_name") if state_data.get("reg_last_name") else message.from_user.last_name
    text = (f'Имя: {first_name if first_name else "не указано"}\n'
            f'Фамилия: {last_name if last_name else "не указано"}\n'
            f'Верно? Нажмите "Изменить" для корректировки данных')
    if not first_name or not last_name:
        text += "\nПожалуйста, если не сложно, добавьте отсуствующие данные"
    await message.answer(text=text,
                         reply_markup=get_rm_by_str([
                             "Подтвердить",
                             "Изменить",
                             "Вернуться к табельному номеру"
                         ]))
    await state.set_state(RegistrationFSM.ask_name)


async def f_registration_change_name(message: types.Message, state: FSMContext):
    full_name = message.text.split(" ")
    if len(full_name) == 2:
        await state.update_data(reg_first_name=full_name[1])
        await state.update_data(reg_last_name=full_name[0])
        await f_registration_ask_name(message, state)
    else:
        await message.answer(text="Что-то не так. Вам нужно ввести фамилию и имя через пробел\n"
                                  "Нарпример, Иванов Иван")


async def f_registration_set_name(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    if not state_data.get("reg_first_name"):
        await state.update_data(
            reg_first_name=message.from_user.first_name if message.from_user.first_name else "Неизвестно",
        )
    if not state_data.get("reg_last_name"):
        await state.update_data(
            reg_last_name=message.from_user.last_name if message.from_user.last_name else "Неизвестно",
        )
    await message.answer(text="Отлично! С этим разобрались. Давайте теперь определимся, с какого ОСП Вы работаете\n"
                         "От этого зависит выдача автомобилей, контактов и другой информации",
                         reply_markup=get_rm_by_str(['Вернуться к имени']))
    await f_registration_ask_city(message.from_user.id, state)


async def f_registration_ask_city(tg_id: int, state: FSMContext):
    cities = [{"id": city.id,
               "name": city.name} async for city in City.objects.all()]
    await bot.send_message(chat_id=tg_id,
                           text="Для начала выберите город",
                           reply_markup=get_city_buttons(cities))
    await state.set_state(RegistrationFSM.ask_city)


async def f_registration_ask_base(tg_id: int, state: FSMContext):
    state_data = await state.get_data()
    city_id = state_data.get("reg_city")
    if not city_id:
        await f_registration_ask_city(tg_id, state)
        return
    bases = [{"id": base.id,
               "name": base.name} async for base in Base.objects.filter(city_id=city_id)]
    await bot.send_message(chat_id=tg_id,
                           text="Теперь выберите ваш ОСП",
                           reply_markup=get_bases_buttons(bases))
    await state.set_state(RegistrationFSM.ask_base)


async def f_registration_add_user(tg_id: int, state: FSMContext):
    state_data = await state.get_data()
    user = await NewUser.objects.acreate(
        username=f'driver{tg_id}',
        first_name=state_data.get("reg_first_name") if state_data.get("reg_first_name") else "Неизвестно",
        last_name=state_data.get("reg_last_name") if state_data.get("reg_last_name") else "Неизвестно",
        password=make_password(get_random_password(8)),
        dellin_service_number=state_data.get("reg_service_number"),
        base_id=state_data.get("reg_base"),
        telegram_id=tg_id,
    )
    await user.groups.aadd(await Group.objects.aget(name="MKTDriver"))
    await bot.send_message(chat_id=tg_id,
                           text="Вы успешно зарегистрировались! Если при регистрации было "
                                "введено что-то неверно, ничего страшного. Вы всегда можете "
                                "поменять свои данные в настройках")
    await send_menu(tg_id, state)
