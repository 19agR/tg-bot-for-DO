import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message

token = '6857731639:AAFhSrrHn1kJBck4XaXPguipZ_iIEwMDgdM'

bot = Bot(token)
dp = Dispatcher()


@dp.message()
async def start(message: Message):
    await message.copy_to(chat_id=message.chat.id)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
