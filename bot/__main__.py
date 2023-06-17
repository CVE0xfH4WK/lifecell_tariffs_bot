import asyncio

from aiogram import Bot, Dispatcher

from bot.handlers import router
from data.db import init_connection
from shared.config import config
from shared.logger import setup_loggers


async def main():
    await init_connection()

    dp = Dispatcher()
    dp.include_router(router)

    bot = Bot(config.telegram.bot_token, parse_mode='HTML')

    await dp.start_polling(bot)


if __name__ == "__main__":
    setup_loggers()

    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
