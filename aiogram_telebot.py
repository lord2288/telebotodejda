import asyncio
from aiogram import Bot, Dispatcher
from app import key
from app.hendlers import router


bot = Bot(token=key.telebot_api)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())