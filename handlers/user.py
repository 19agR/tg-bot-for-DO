from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from keyboards.buttons import *
from keyboards.reply_keyboards import main_user
from utils.filters import IsNotAdmin

router = Router()


@router.message(CommandStart(), IsNotAdmin())
async def start(message: Message):
    text = open('data/texts/greet_user.txt', encoding='utf-8').read()
    await message.answer(text, reply_markup=main_user())

    print(message.from_user.id, message.from_user.username)


# @router.message(F.text.lower() == LIST_AVAILABLE_CURSES.lower(), IsNotAdmin())
# async def list_available_curses(message: Message):



@router.message(F.text.lower() == MY_CURSES.lower(), IsNotAdmin())
async def my_curses(message: Message):
    await message.answer('Скоро здесь будет список курсов, на которые Вы записаны')


@router.message(F.text.lower() == HELP.lower(), IsNotAdmin())
async def faq(message: Message):
    await message.answer('Скоро здесь будут ответы на вопросы')


@router.message(F.text.lower() == NOTIFICATIONS.lower(), IsNotAdmin())
async def notifications(message: Message):
    await message.answer('Скоро здесь будет редактировать уведомления')
