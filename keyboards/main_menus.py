from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.buttons import *


def build_reply_keyboard(buttons: list[list]):
    buttons_to_add = [[KeyboardButton(text=text) for text in row] for row in buttons]
    return ReplyKeyboardMarkup(keyboard=buttons_to_add, resize_keyboard=True)


def main_user():
    buttons = [
        [KeyboardButton(text=LIST_AVAILABLE_CURSES)],
        [KeyboardButton(text=MY_CURSES), KeyboardButton(text=HELP), KeyboardButton(text=NOTIFICATIONS)]
    ]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def main_admin():
    buttons = [
        [KeyboardButton(text=REQUESTS), KeyboardButton(text=REDACT_CURSES)],
        [KeyboardButton(text=REDACT_HELP)]
    ]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def redact_curses_menu():
    buttons = [
        [KeyboardButton(text=CREATE_NEW_COURSE), KeyboardButton(text=VIEW_COURSES)],
        [KeyboardButton(text=ADD_NEW_TEACHER), KeyboardButton(text=BACK)],
    ]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


