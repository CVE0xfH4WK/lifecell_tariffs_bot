from aiogram import Router
from aiogram.filters import Command
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_menu_reply_markup() -> ReplyKeyboardMarkup:
    buttons = [
        "Всі тарифи", "Обрати тариф",
        "Про нас"
    ]

    builder = ReplyKeyboardBuilder()
    for button in buttons:
        builder.add(KeyboardButton(text=button))
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


router = Router()
@router.message(Command(commands=["start"]))
async def start(message: Message):
    menu_markup = get_menu_reply_markup()
    lines = [
        f"Вітаю, {message.from_user.first_name}.",
        "Я - Lifecell Bot, офіційний бот компанії-оператора Lifecell.",
        "Щоб розпочати оберіть опцію з меню"
    ]

    await message.answer(
        text='\n'.join(lines),
        reply_markup=menu_markup
    )