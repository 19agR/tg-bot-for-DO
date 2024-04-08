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