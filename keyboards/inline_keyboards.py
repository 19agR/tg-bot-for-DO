from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.buttons import BACK, STAY
from utils.mini_functions import pages_info


def inline_remove_message():
    buttons = [
        [InlineKeyboardButton(text='Закрыть', callback_data='remove_message')]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def show_teachers(redact=False):
    if redact:
        buttons = [
            [InlineKeyboardButton(text='Список преподавателей', callback_data='show_teachers')],
            [InlineKeyboardButton(text=STAY, callback_data='stay_teacher')]
        ]
    else:
        buttons = [
            [InlineKeyboardButton(text='Список преподавателей', callback_data='show_teachers')]
        ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


class PaginationCourses(CallbackData, prefix='pag_courses'):
    action: str
    page: int


def paginator_courses(page: int = 1):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=f'Выбрать курс | {pages_info(page)}', callback_data=PaginationCourses(action='select', page=page).pack()))
    builder.row(
        InlineKeyboardButton(text='⬅️', callback_data=PaginationCourses(action='prev', page=page).pack()),
        InlineKeyboardButton(text='➡️', callback_data=PaginationCourses(action='next', page=page).pack()),
    )
    return builder.as_markup()
