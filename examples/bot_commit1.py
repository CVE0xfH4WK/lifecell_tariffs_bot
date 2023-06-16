import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command, Text
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


TOKEN = "BOT_TOKEN"

router = Router()


@router.message(Command(commands=["start"]))
async def start(message: Message):
    buttons = [
        "Про нас", "Обрати тариф"
    ]

    builder = ReplyKeyboardBuilder()
    for button in buttons:
        builder.add(KeyboardButton(text=button))
    builder.adjust(2)

    await message.answer(f"Вітаю, {message.from_user.first_name}."
                         f"\nЯ - Lifecell Bot, офіційний бот компанії-оператора Lifecell."
                         f"\nОберіть дію, для того, щоб продорвжити : ",
                         reply_markup=builder.as_markup(resize_keyboard=True))

@router.message(Text("Про нас"))
async def info(message: Message):
    await message.answer("тут буде інформація..")


@router.message(Text("Обрати тариф"))
async def choose_tariff(message: Message):
    builder = InlineKeyboardBuilder()

    for i in range(3):
        builder.add(InlineKeyboardButton(
            text=f"option {i+1}",
            callback_data=f"option_choice_{i+1}"
        ))

    await message.answer(
        "Оберіть одну з опцій, (test options)",
        reply_markup=builder.as_markup()
    )


@router.callback_query(Text("option_choice_1"))
async def opt_1(callback: CallbackQuery):
    await callback.message.answer("opt 1")
    await callback.answer()


@router.callback_query(Text("option_choice_2"))
async def opt_1(callback: CallbackQuery):
    await callback.message.answer("opt 2")
    await callback.answer()


@router.callback_query(Text("option_choice_3"))
async def opt_1(callback: CallbackQuery):
    await callback.message.answer("opt 3")
    await callback.answer()


async def main():
    dp = Dispatcher()
    dp.include_router(router)

    bot = Bot(TOKEN, parse_mode='HTML')

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
