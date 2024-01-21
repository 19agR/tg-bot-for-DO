from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.buttons import BACK
from utils.mini_functions import pages_info


def inline_remove_message():
    buttons = [
        [InlineKeyboardButton(text='Закрыть', callback_data='remove_message')]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def show_teachers():
    buttons = [
        [InlineKeyboardButton(text='Список преподавателей', callback_data='show_teachers'),
         InlineKeyboardButton(text=BACK, callback_data='inline_back')]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


class PaginationCourses(CallbackData, prefix='pag_courses'):
    action: str
    page: int


def paginator_courses(page: int = 1):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='⬅️', callback_data=PaginationCourses(action='prev', page=page).pack()),
        InlineKeyboardButton(text=pages_info(page), callback_data=PaginationCourses(action='info', page=page).pack()),
        InlineKeyboardButton(text='➡️', callback_data=PaginationCourses(action='next', page=page).pack()),
    )
    return builder.as_markup()
