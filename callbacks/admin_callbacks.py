from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.admin import add_new_teacher_cancel
from keyboards.inline_keyboards import inline_remove_message, PaginationCourses, paginator_courses
from keyboards.reply_keyboards import redact_curses_menu
from utils.db import db
from utils.mini_functions import print_course

router = Router()


@router.callback_query(F.data == 'show_teachers')
async def callback_show_teachers(call: CallbackQuery):
    teachers = db.select_teachers()
    prepared_text = '\n'.join(f'<b><i>ID:</i></b> {t[0]}; <b><i>ФИО:</i></b> {t[1]}' for t in teachers)

    await call.message.answer(prepared_text, reply_markup=inline_remove_message())
    await call.answer()


@router.callback_query(F.data == 'inline_back')
async def callback_inline_back(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text('Создание нового курса отменено.\n'
                                 'Выберите дальнейшее действие в меню')
    await call.answer()


@router.callback_query(F.data == 'remove_message')
async def callback_remove_message(call: CallbackQuery):
    await call.message.delete()


@router.callback_query(PaginationCourses.filter(F.action.in_(['prev', 'next'])))
async def callback_for_pagination_courses(call: CallbackQuery, callback_data: PaginationCourses):
    action, cur_page = callback_data.action, callback_data.page
    quantity = db.quantity_courses
    next_page = cur_page + 1 if action == 'next' else cur_page - 1

    if next_page <= 0:
        next_page = quantity
    elif next_page == quantity + 1:
        next_page = 1

    course = db.select_courses()[next_page - 1]

    await call.message.edit_text(print_course(course), reply_markup=paginator_courses(next_page))


@router.callback_query(PaginationCourses.filter(F.action == 'info'))
async def callback_pag_info(call: CallbackQuery):
    await call.answer()
