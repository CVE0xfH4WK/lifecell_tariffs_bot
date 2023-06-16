import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.handlers import router
from config import config


async def main():
    dp = Dispatcher()
    dp.include_router(router)

    bot = Bot(config.telegram.bot_token, parse_mode='HTML')

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
