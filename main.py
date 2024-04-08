import asyncio
from aiogram import Bot, Dispatcher
from handlers import user, admin
from callbacks import admin_callbacks, user_callbacks, other_callbacks

token = '6760277917:AAGnmInTf_B3mgEs9Yo6OoALtjtfbDPWq1k'

bot = Bot(token, parse_mode='HTML')
dp = Dispatcher()

dp.include_routers(
    user.router,
    admin.router,
    admin_callbacks.router,
    user_callbacks.router,
    other_callbacks.router,
)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
