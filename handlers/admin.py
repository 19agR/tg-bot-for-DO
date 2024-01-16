from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from keyboards.buttons import *
from keyboards.main_menus import main_admin
from utils.filters import IsAdmin

router = Router()


@router.message(CommandStart(), IsAdmin())
async def start(message: Message):
    text = open('data/texts/greet_admin.txt', encoding='utf-8').read()
    await message.answer(text, reply_markup=main_admin())


@router.message(F.text.lower() == REQUESTS.lower(), IsAdmin())
async def list_available_curses(message: Message):
    await message.answer('Скоро здесь будут заявки на запись от пользователей')


@router.message(F.text.lower() == REDACT_HELP.lower(), IsAdmin())
async def list_available_curses(message: Message):
    await message.answer('Скоро здесь можно будет редактировать вкладку "Помощь"')


@router.message(F.text.lower() == REDACT_CURSES.lower(), IsAdmin())
async def list_available_curses(message: Message):
    await message.answer('Скоро здесь можно будет добавлять новые курсы или редактировать уже существующие')

