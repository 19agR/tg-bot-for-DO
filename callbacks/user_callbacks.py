from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.admin import add_new_teacher_cancel, create_new_course, create_course_teacher_id
from keyboards.buttons import BACK
from keyboards.inline_keyboards import inline_remove_message, PaginationCourses, paginator_courses
from keyboards.reply_keyboards import redact_curses_menu, build_reply_keyboard
from utils.db import db
from utils.filters import IsAdmin, IsNotAdmin
from utils.mini_functions import print_course
from utils.states import CreateCourse, SelectCourseByUser

router = Router()


@router.callback_query(PaginationCourses.filter(F.action == 'select'), IsNotAdmin())
async def callback_pag_info(call: CallbackQuery, callback_data: PaginationCourses, state: FSMContext):
    cur_page = callback_data.page
    course = db.select_courses()[cur_page - 1]
    course_id = course[0]
    teacher_name = db.select_teacher(course[1])[1]
    course_name = course[2]

    await state.set_state(SelectCourseByUser.full_name)
    await state.update_data(course_id=course_id)
    await state.update_data(course_name=course_name)
    await state.update_data(teacher_name=teacher_name)
    await call.message.answer(f'Вы выбрали курс "{course_name}" с преподавателем {teacher_name}.\n\n'
                              f'Для оформления заявки нам необходимы ваши:\n'
                              f'- ФИО\n'
                              f'- Номер телефона\n\n'
                              f'Для начала, пожалуйста, введите Фамилию, Имя и Отчество',
                              reply_markup=build_reply_keyboard([[BACK]]))

    await call.answer()
