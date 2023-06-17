import asyncio

from aiogram import Dispatcher

from bot.bot import bot
from bot.handlers import router
from bot.logics import closest_value
from data.db import init_connection
from shared.logger import setup_loggers


async def main():
    await init_connection()
    await closest_value()

    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    setup_loggers()

    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
