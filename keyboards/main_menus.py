from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.buttons import *


def main_user():
    buttons = [
        [KeyboardButton(text=LIST_AVAILABLE_CURSES)],
        [KeyboardButton(text=MY_CURSES), KeyboardButton(text=HELP), KeyboardButton(text=NOTIFICATIONS)]
    ]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def main_admin():
    buttons = [
        [KeyboardButton(text=REQUESTS), KeyboardButton(text=REDACT_HELP)],
        [KeyboardButton(text=REDACT_CURSES)]
    ]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
