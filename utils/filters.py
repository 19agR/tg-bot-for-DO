from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

admins = [int(line) for line in open('data/admins.txt')]


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message):
        return message.from_user.id in admins


class IsNotAdmin(BaseFilter):
    async def __call__(self, message: Message):
        return message.from_user.id not in admins


class IsNoneState(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        return await state.get_state() is None
