import asyncio
from aiogram import Bot, Dispatcher
from handlers import user, admin
from callbacks import admin_callbacks

token = '6857731639:AAFhSrrHn1kJBck4XaXPguipZ_iIEwMDgdM'

bot = Bot(token, parse_mode='HTML')
dp = Dispatcher()

dp.include_routers(
    user.router,
    admin.router,
    admin_callbacks.router
)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
