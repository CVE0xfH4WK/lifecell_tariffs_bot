from src.handler import router

import asyncio
import logging

from aiogram import Bot, Dispatcher, Router

from src.config import TOKEN


async def main():
    dp = Dispatcher()
    dp.include_router(router)

    bot = Bot(TOKEN, parse_mode='HTML')

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
