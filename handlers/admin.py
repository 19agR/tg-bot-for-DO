from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from keyboards.buttons import *
from keyboards.inline_keyboards import show_teachers, paginator_courses, inline_request_accept
from keyboards.reply_keyboards import main_admin, redact_curses_menu, build_reply_keyboard, main_user
from utils.filters import IsAdmin, IsNoneState, admins
from utils.mini_functions import print_course
from utils.states import AddNewTeacher, CreateCourse

from utils.db import db

router = Router()


@router.message(Command(commands='user'), IsAdmin())
async def start(message: Message):
    if message.from_user.id in admins:
        admins.remove(message.from_user.id)
    await message.answer('Вам выданы права обычного пользователя', reply_markup=main_user())


@router.message(CommandStart(), IsNoneState(), IsAdmin())
async def start(message: Message):
    text = open('data/texts/greet_admin.txt', encoding='utf-8').read()
    await message.answer(text, reply_markup=main_admin())


@router.message(F.text.lower() == BACK.lower(), IsNoneState(), IsAdmin())
async def back_to_main_menu(message: Message):
    await message.answer('Вы вернулись в главное меню администратора.\n'
                         'Выберите одну из кнопок ниже', reply_markup=main_admin())


@router.message(F.text.lower() == REQUESTS.lower(), IsAdmin())
async def requests(message: Message):
    student_requests = db.select_requests()
    await message.answer(f'Количество заявок: {len(student_requests)}')

    for i, student_request in enumerate(student_requests):
        course_id = int(student_request[5].split()[-1])
        course = db.select_course(course_id)
        course_name = course[2]
        course_teacher = db.select_teacher(course[1])[1]
        student_name = student_request[1]
        student_phone_number = student_request[2]
        student_tg_user_id = student_request[3]
        student_tg_username = student_request[4]

        await message.answer(f'<b>Заявка #{i + 1}</b>\n\n'
                             f'Данные ученика:\n'
                             f'Имя: {student_name};\n'
                             f'Номер: {student_phone_number};\n'
                             f'TG: @{student_tg_username}\n\n'
                             f'Желает записаться на курс "{course_name}" к преподавателю {course_teacher}',
                             reply_markup=inline_request_accept(student_tg_user_id, course_id)
                             )



@router.message(F.text.lower() == REDACT_HELP.lower(), IsAdmin())
async def redact_faq(message: Message):
    await message.answer('Скоро здесь можно будет редактировать вкладку "Помощь"')


@router.message(F.text.lower() == REDACT_CURSES.lower(), IsAdmin())
async def redact_curses(message: Message):
    await message.answer('Вы вошли в меню редактирования курсов и преподавателей.\n'
                         'Выберите дальнейшее действие в меню',
                         reply_markup=redact_curses_menu())


"""   ---Add Teacher START---   """


@router.message(F.text.lower() == ADD_NEW_TEACHER.lower(), IsAdmin())
async def add_new_teacher(message: Message, state: FSMContext):
    await state.set_state(AddNewTeacher.full_name)
    await message.answer('Вы зашли в форму добавления нового преподавателя. \n'
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
                         f'<b><i>ФИО:</i></b> {data["full_name"]}\n'
                         f'<b><i>Номер телефона:</i></b> {data["phone_number"]}\n\n'
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


"""   ---Add Teacher THE END---   """

"""   ---Add Course START---   """


@router.message(F.text.lower() == BACK.lower(), CreateCourse(), IsAdmin())
async def add_new_course_cancel(message: Message, state: FSMContext):
    data = await state.get_data()
    if 'course_to_redact' in data:
        db.redact_course(data)
        await message.answer('Редактирование курса завершено. Все изменения сохранены.\n'
                             'Выберите дальнейшее действие в меню',
                             reply_markup=redact_curses_menu())
    else:
        await message.answer('Создание нового курса отменено.\n'
                             'Выберите дальнейшее действие в меню',
                             reply_markup=redact_curses_menu())
    await state.clear()


@router.message(F.text.lower() == CREATE_NEW_COURSE.lower(), IsAdmin())
async def create_new_course(message: Message, state: FSMContext):
    await state.set_state(CreateCourse.teacher_id)

    data = await state.get_data()
    if 'course_to_redact' in data:
        course = data['course_to_redact']
        course_id = course[0]
        teacher_id = course[1]
        teacher_name = db.select_teacher(teacher_id)[1]
        name = course[2]
        description = course[3]
        cost_per_month = course[4]
        type_course = course[5]
        available_places = course[6]
        timetable = course[7]

        await state.update_data(
            course_id=course_id,
            teacher_id=teacher_id,
            name=name,
            description=description,
            cost_per_month=cost_per_month,
            type_course=type_course,
            available_places=available_places,
            timetable=timetable,
        )

        text = (f'Вы выбрали курс "{name}" с преподавателем {teacher_name} для редактирования. \n'
                f'Если вы хотите оставить текущего преподавателя, то нажмите кнопку "Оставить"\n\n'
                f'Если же вы хотите сменить преподавателя курса, то ')
    else:
        text = 'Вы зашли в форму создания нового курса. \n'

    text += ('<b>Введите ID преподавателя</b>, который будет вести этот курс.\n\n'
             'Если Вы не помните ID нужного преподавателя, '
             'то можете воспользоваться кнопкой ниже для просмотра ID всех преподавателей.\n\n'
             'Вы можете воспользоваться кнопкой назад для отмены действия и выхода в меню.')

    await message.answer(text, reply_markup=show_teachers(redact='course_to_redact' in data))


@router.message(F.text, CreateCourse.teacher_id, IsAdmin())
async def create_course_teacher_id(message: Message, state: FSMContext, stay=False):
    data = await state.get_data()

    if 'course_to_redact' in data and stay:
        await state.set_state(CreateCourse.name)

        await message.answer(f'Отлично! Преподаватель остался без изменений.\n\n'
                             'Теперь введите новое название курса или нажмите кнопку "Оставить"',
                             reply_markup=build_reply_keyboard([[STAY, BACK]]))

        return

    if not message.text.isdigit():
        await message.answer('ID Преподавателя должно быть числом. Попробуйте снова.\n\n'
                             'Вы можете воспользоваться кнопкой назад для отмены действия и выхода в меню.',
                             reply_markup=build_reply_keyboard([[BACK]]))
        return

    teacher_id = int(message.text)
    await state.update_data(teacher_id=teacher_id)
    await state.set_state(CreateCourse.name)

    teacher_name = db.select_teacher(teacher_id)[1]

    if 'course_to_redact' in data:
        await message.answer(f'Отлично! {teacher_name} выбран как преподаватель для этого курса.\n\n'
                             'Теперь введите новое название курса или нажмите кнопку "Оставить"',
                             reply_markup=build_reply_keyboard([[STAY, BACK]]))
    else:
        await message.answer(f'Отлично! {teacher_name} выбран как преподаватель для этого курса.\n\n'
                             'Теперь введите название курса.',
                             reply_markup=build_reply_keyboard([[BACK]]))


@router.message(F.text, CreateCourse.name, IsAdmin())
async def create_course_name(message: Message, state: FSMContext):
    await state.set_state(CreateCourse.description)

    if message.text.lower() == 'оставить':
        await message.answer('Название осталось без изменений. Введите новое описание для этого курса или нажмите '
                             '"Оставить".\n'
                             'Если вы закончили изменения, нажмите кнопку "Назад"',
                             reply_markup=build_reply_keyboard([[STAY, BACK]]))
        return

    data = await state.get_data()
    kb = build_reply_keyboard([[STAY, BACK]]) if 'course_to_redact' in data else build_reply_keyboard([[BACK]])

    await state.update_data(name=message.text)
    await message.answer('Название сохранено. Введите подробное описание для этого курса.',
                         reply_markup=kb)


@router.message(F.text, CreateCourse.description, IsAdmin())
async def create_course_description(message: Message, state: FSMContext):
    await state.set_state(CreateCourse.cost_per_month)

    if message.text.lower() == 'оставить':
        await message.answer('Описание осталось без изменений. Укажите, пожалуйста, новую стоимость в месяц для этого '
                             'курса или нажмите кнопку "Оставить".',
                             reply_markup=build_reply_keyboard([[STAY, BACK]]))
        return

    data = await state.get_data()
    kb = build_reply_keyboard([[STAY, BACK]]) if 'course_to_redact' in data else build_reply_keyboard([[BACK]])

    await state.update_data(description=message.text)
    await message.answer('Описание сохранено. Укажите, пожалуйста, стоимость в месяц для этого курса.',
                         reply_markup=kb)


@router.message(F.text, CreateCourse.cost_per_month, IsAdmin())
async def create_course_cost_per_month(message: Message, state: FSMContext):
    if message.text.lower() == 'оставить':
        await state.set_state(CreateCourse.type_course)
        await message.answer('Стоимость курса осталась без изменений. Теперь укажите тип курса:\n'
                             '- Индивидуальные занятия\n'
                             '- Групповые занятия',
                             reply_markup=build_reply_keyboard([
                                 ['Индивидуальные', 'Групповые'],
                                 [BACK]
                             ]))
        return

    if not message.text.isdigit():
        await message.answer('Стоимость должна быть числом. Попробуйте снова.\n\n'
                             'Вы можете воспользоваться кнопкой назад для отмены действия и выхода в меню.',
                             reply_markup=build_reply_keyboard([[BACK]]))
        return

    await state.update_data(cost_per_month=int(message.text))
    await state.set_state(CreateCourse.type_course)

    await message.answer('Указанная стоимость сохранена. Теперь укажите тип курса:\n'
                         '- Индивидуальные занятия\n'
                         '- Групповые занятия',
                         reply_markup=build_reply_keyboard([
                             ['Индивидуальные', 'Групповые'],
                             [BACK]
                         ]))


@router.message(F.text, CreateCourse.type_course, IsAdmin())
async def create_course_type_course(message: Message, state: FSMContext):
    text = message.text.lower()
    if 'индивид' in text:
        type_course = 'Индивидуальные занятия'
        await state.update_data(type_course=type_course, available_places=None, timetable=None)
        await state.set_state(CreateCourse.accept)

        data = await state.get_data()
        teacher_name = db.select_teacher(data['teacher_id'])[1]
        data_to_accept = (f'<i><b>Преподаватель:</b></i> {teacher_name} (id: {data["teacher_id"]})\n'
                          f'<i><b>Название:</b></i> {data["name"]}\n'
                          f'<i><b>Описание:</b></i> {data["description"]}\n'
                          f'<i><b>Стоимость в месяц:</b></i> {data["cost_per_month"]}₽\n'
                          f'<i><b>Тип курса:</b></i> {data["type_course"]}\n')

        await message.answer('Отлично! Почти все готово. Осталось сверить и подтвердить введенные данные.\n\n'
                             f'{data_to_accept}\n\n'
                             f'Воспользуйтесь клавиатурой ниже, чтобы подтвердить или отменить добавление нового курса',
                             reply_markup=build_reply_keyboard([[ACCEPT, BACK]]))

    elif 'групп' in text:
        type_course = 'Групповые занятия'
        await state.update_data(type_course=type_course)
        await state.set_state(CreateCourse.available_places)

        data = await state.get_data()
        hint = data.get('available_places', False)
        kb = build_reply_keyboard([[hint, BACK]]) if hint else build_reply_keyboard([[BACK]])

        await message.answer('Отлично! Осталось еще немного.\n\n '
                             'Укажите, пожалуйста, количество доступных мест в группе.',
                             reply_markup=kb)
    else:
        await message.answer('К сожалению, я Вас я не понимаю. Введите: "Индивидуальные" или "Групповые"'
                             ' или нажмите на соответствующую кнопку.\n\n'
                             'Также Вы можете воспользоваться кнопкой назад для отмены действия и выхода в меню.',
                             reply_markup=build_reply_keyboard([[BACK]]))
        return


@router.message(F.text, CreateCourse.available_places, IsAdmin())
async def create_course_available_places(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Количество доступных мест в группе должно быть числом. Попробуйте снова.\n\n'
                             'Вы можете воспользоваться кнопкой назад для отмены действия и выхода в меню.',
                             reply_markup=build_reply_keyboard([[BACK]]))
        return

    await state.set_state(CreateCourse.timetable)
    await state.update_data(available_places=int(message.text))

    data = await state.get_data()
    cur_timetable = 'timetable' in data
    text = ', или нажмите кнопку "Оставить"' if cur_timetable else ''

    await message.answer('Введите расписание для данной группы, если оно уже утверждено или "Нет" в случае, '
                         f'если действующего расписания еще нет{text}\n\n'
                         'Желательный формат расписания:\n'
                         '<День недели> - <Время в часах и минутах>\n\n'
                         'Вы можете воспользоваться кнопкой назад для отмены действия и выхода в меню.',
                         reply_markup=build_reply_keyboard([[STAY, 'Расписания еще нет'], [BACK]]), parse_mode=None)


@router.message(F.text, CreateCourse.timetable, IsAdmin())
async def create_course_timetable(message: Message, state: FSMContext):
    if 'нет' in message.text:
        await state.update_data(timetable=None)
    elif message.text.lower() != 'оставить':
        await state.update_data(timetable=message.text)

    await state.set_state(CreateCourse.accept)
    data = await state.get_data()
    teacher_name = db.select_teacher(data['teacher_id'])[1]
    data_to_accept = (f'<b><i>Преподаватель:</i></b> {teacher_name} (id: {data["teacher_id"]})\n'
                      f'<b><i>Название:</i></b> {data["name"]}\n'
                      f'<b><i>Описание:</i></b> {data["description"]}\n'
                      f'<b><i>Стоимость в месяц:</i></b> {data["cost_per_month"]}₽\n'
                      f'<b><i>Тип курса:</i></b> {data["type_course"]}\n'
                      f'<b><i>Доступное количество мест:</i></b> {data["available_places"]}\n'
                      f'<b><i>Расписание:</i></b> '
                      f'{timetable if (timetable := data["timetable"]) is not None else "отсутствует"}')

    await message.answer('Отлично! Почти все готово. Осталось сверить и подтвердить введенные данные.\n\n'
                         f'{data_to_accept}\n\n'
                         f'Воспользуйтесь клавиатурой ниже, чтобы подтвердить или отменить добавление нового курса',
                         reply_markup=build_reply_keyboard([[ACCEPT, BACK]]))


@router.message(F.text.lower() == ACCEPT.lower(), CreateCourse.accept, IsAdmin())
async def create_course_accept(message: Message, state: FSMContext):
    data = await state.get_data()

    if 'course_to_redact' in data:
        db.redact_course(data)
    else:
        db.add_course(data)

    await message.answer('Данные о курсе успешно внесены в базу данных!',
                         reply_markup=main_admin())


"""   ---Add Course THE END---   """

"""   ---View Courses START---   """


@router.message(F.text.lower() == VIEW_COURSES.lower(), IsAdmin())
async def view_courses(message: Message):
    course = db.select_courses()[0]
    await message.answer(print_course(course),
                         reply_markup=paginator_courses())
