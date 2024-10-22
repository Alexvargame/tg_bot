import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import settings

from routers import router as main_router




async def main():
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    dp.include_router(main_router)
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
