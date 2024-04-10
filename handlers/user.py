import re

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from keyboards.buttons import *
from keyboards.inline_keyboards import paginator_courses
from keyboards.reply_keyboards import main_user, build_reply_keyboard, main_admin

from utils.db import db
from utils.filters import IsNotAdmin, IsNoneState, admins
from utils.mini_functions import print_course
from utils.states import SelectCourseByUser

router = Router()


@router.message(Command(commands='admin'), IsNotAdmin())
async def start(message: Message):
    admins.append(message.from_user.id)
    await message.answer('Вам выданы права администратора', reply_markup=main_admin())


@router.message(CommandStart(), IsNotAdmin())
async def start(message: Message):
    text = open('data/texts/greet_user.txt', encoding='utf-8').read()
    await message.answer(text, reply_markup=main_user())

    print(message.from_user.id, message.from_user.username)


@router.message(F.text.lower() == BACK.lower(), IsNotAdmin())
async def back_to_main_menu(message: Message):
    await message.answer('Вы вернулись в главное меню.\n'
                         'Выберите одну из кнопок ниже', reply_markup=main_user())


"""   ---Select Course START---   """


@router.message(F.text.lower() == LIST_AVAILABLE_CURSES.lower(), IsNotAdmin())
async def list_available_curses(message: Message):
    courses = db.select_courses()
    if courses:
        course = courses[0]
        await message.answer(print_course(course),
                             reply_markup=paginator_courses())
    else:
        await message.answer('К сожалению, администраторами не было добавлено еще ни одного курса. Попробуйте позже')


@router.message(F.text, SelectCourseByUser.full_name, IsNotAdmin())
async def select_course_full_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await state.set_state(SelectCourseByUser.phone_number)

    await message.answer(f'Ваше ФИО сохранено. Осталось ввести номер телефона для возможности обратной связи '
                         f'администратора с вами.\n'
                         f'Следующим сообщением введите номер телефона в формате: +7(XXX)XXX-XX-XX',
                         reply_markup=build_reply_keyboard([[BACK]]))


@router.message(F.text, SelectCourseByUser.phone_number, IsNotAdmin())
async def select_course_phone_number(message: Message, state: FSMContext):
    phone_number = message.text

    if re.match(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', phone_number) is None:
        await message.answer('Боюсь, что вы ввели не номер телефона или ввели его в неизвестном для меня формате :(\n'
                             'Попробуйте, пожалуйста, еще раз!')

        return

    await state.update_data(phone_number=phone_number)
    await state.set_state(SelectCourseByUser.accept)

    data = await state.get_data()

    await message.answer(f'Данные сохранены. Осталось лишь все проверить!\n'
                         f'Сверьте данные и нажмите кнопку "Подтвердить", '
                         f'если все верно и Вы хотите отправить заявку\n\n'
                         f'Вы хотите записаться на курс \"{data["course_name"]}\", который преподает {data["teacher_name"]}\n\n'
                         f'Ваши данные:\n'
                         f'<b><i>ФИО:</i></b> {data["name"]}\n'
                         f'<b><i>Номер телефона:</i></b> {data["phone_number"]}\n\n'
                         'Если хотите отменить запись, нажмите "Назад"',
                         reply_markup=build_reply_keyboard([[ACCEPT, BACK]]))


@router.message(F.text.lower() == ACCEPT.lower(), SelectCourseByUser.accept, IsNotAdmin())
async def select_course_accept(message: Message, state: FSMContext):
    data = await state.get_data()
    data['tg_user_id'] = message.from_user.id
    data['tg_username'] = message.from_user.username
    await state.clear()
    result = db.add_course_to_user(data)
    if result:
        await message.answer('Заявка отправлена. Ожидайте обратного звонка от администратора в рабочие часы центра.',
                             reply_markup=main_user())
    else:
        await message.answer('Возникла ошибка в переданных данных. Заявка не была отправлена.',
                             reply_markup=main_user())


"""   ---Select Course THE END---   """


@router.message(F.text.lower() == MY_CURSES.lower(), IsNotAdmin())
async def my_curses(message: Message):
    await message.answer('Скоро здесь будет список курсов, на которые Вы записаны')


@router.message(F.text.lower() == HELP.lower(), IsNotAdmin())
async def faq(message: Message):
    await message.answer('Скоро здесь будут ответы на вопросы')


@router.message(F.text.lower() == NOTIFICATIONS.lower(), IsNotAdmin())
async def notifications(message: Message):
    await message.answer('Скоро здесь будет редактировать уведомления')
