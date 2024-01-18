from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from keyboards.buttons import *
from keyboards.main_menus import main_admin, redact_curses_menu, build_reply_keyboard
from utils.filters import IsAdmin, IsNoneState
from utils.states import AddNewTeacher

from utils.db import db

router = Router()


@router.message(CommandStart(), IsAdmin())
async def start(message: Message):
    text = open('data/texts/greet_admin.txt', encoding='utf-8').read()
    await message.answer(text, reply_markup=main_admin())


@router.message(F.text.lower() == BACK.lower(), IsNoneState(), IsAdmin())
async def back_to_main_menu(message: Message):
    await message.answer('Вы вернулись в главное меню администратора.\n'
                         'Выберите одну из кнопок ниже', reply_markup=main_admin())


@router.message(F.text.lower() == REQUESTS.lower(), IsAdmin())
async def requests(message: Message):
    await message.answer('Скоро здесь будут заявки на запись от пользователей')


@router.message(F.text.lower() == REDACT_HELP.lower(), IsAdmin())
async def redact_faq(message: Message):
    await message.answer('Скоро здесь можно будет редактировать вкладку "Помощь"')


@router.message(F.text.lower() == REDACT_CURSES.lower(), IsAdmin())
async def redact_curses(message: Message):
    await message.answer('Вы вошли в меню редактирования курсов и преподавателей.\n'
                         'Выберите дальнейшее действие в меню',
                         reply_markup=redact_curses_menu())


@router.message(F.text.lower() == ADD_NEW_TEACHER.lower(), IsAdmin())
async def add_new_teacher(message: Message, state: FSMContext):
    await state.set_state(AddNewTeacher.full_name)
    await message.answer('Вы зашли в форму создания нового преподавателя. \n'
                         'Введите ФИО преподавателя, которого хотите добавить '
                         'или воспользуйтесь кнопкой назад для отмены действия.',
                         reply_markup=build_reply_keyboard([[BACK]]))


@router.message(F.text.lower() == BACK.lower(), AddNewTeacher(), IsAdmin())
async def add_new_teacher_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Добавление нового преподавателя отменено.\n'
                         'Выберите дальнейшее действие в меню',
                         reply_markup=redact_curses_menu())


@router.message(AddNewTeacher.full_name, IsAdmin())
async def add_new_teacher_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(AddNewTeacher.phone_number)
    await message.answer('Введите номер телефона нового преподавателя '
                         'или воспользуйтесь кнопкой назад для отмены добавления.')


@router.message(AddNewTeacher.phone_number, IsAdmin())
async def add_new_teacher_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    data = await state.get_data()
    await state.set_state(AddNewTeacher.accept)
    await message.answer('Проверьте введенные данные:\n'
                         f'ФИО: {data["full_name"]}\n'
                         f'Номер телефона: {data["phone_number"]}\n\n'
                         'Если все верно, нажмите "Подтвердить". Если хотите отменить добавление, нажмите "Назад"',
                         reply_markup=build_reply_keyboard([[ACCEPT, BACK]]))


@router.message(F.text.lower() == ACCEPT.lower(), AddNewTeacher.accept, IsAdmin())
async def add_new_teacher_accept(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    result = db.add_teacher(data)
    if result:
        await message.answer('Преподаватель был добавлен.', reply_markup=main_admin())
    else:
        await message.answer('Возникла ошибка в переданных данных. Преподаватель не был добавлен.',
                             reply_markup=main_admin())

