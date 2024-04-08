from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.admin import add_new_teacher_cancel, create_new_course, create_course_teacher_id
from keyboards.inline_keyboards import inline_remove_message, PaginationCourses, paginator_courses
from keyboards.reply_keyboards import redact_curses_menu
from utils.db import db
from utils.filters import IsAdmin
from utils.mini_functions import print_course
from utils.states import CreateCourse

router = Router()


@router.callback_query(F.data == 'show_teachers', IsAdmin())
async def callback_show_teachers(call: CallbackQuery):
    teachers = db.select_teachers()
    prepared_text = '\n'.join(f'<b><i>ID:</i></b> {t[0]}; <b><i>ФИО:</i></b> {t[1]}' for t in teachers)

    await call.message.answer(prepared_text, reply_markup=inline_remove_message())
    await call.answer()


@router.callback_query(F.data == 'stay_teacher', IsAdmin())
async def callback_show_teachers(call: CallbackQuery, state: FSMContext):
    await create_course_teacher_id(call.message, state=state, stay=True)
    await call.answer()


# @router.callback_query(F.data == 'inline_back')
# async def callback_inline_back(call: CallbackQuery, state: FSMContext):
#     await state.clear()
#     await call.message.edit_text('Создание нового курса отменено.\n'
#                                  'Выберите дальнейшее действие в меню')
#     await call.answer()


@router.callback_query(F.data == 'remove_message', IsAdmin())
async def callback_remove_message(call: CallbackQuery):
    await call.message.delete()


@router.callback_query(PaginationCourses.filter(F.action == 'select'), IsAdmin())
async def callback_pag_info(call: CallbackQuery, callback_data: PaginationCourses, state: FSMContext):
    cur_page = callback_data.page
    course = db.select_courses()[cur_page - 1]
    await state.update_data(course_to_redact=course)
    await create_new_course(call.message, state)
    await call.answer()
