from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (CallbackQuery, InlineKeyboardButton, KeyboardButton,
                           Message)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


class DB(StatesGroup):
    price = State()
    internet = State()
    signal = State()


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


    # FIXME: The message from user can be undefined, see how it works and fix it
    await message.answer(f"Вітаю, {message.from_user.first_name}."
                         f"\nЯ - Lifecell Bot, офіційний бот компанії-оператора Lifecell."
                         f"\nОберіть дію, для того, щоб продорвжити : ",
                         reply_markup=builder.as_markup(resize_keyboard=True))


@router.message(Text("Про нас"))
async def info(message: Message):
    await message.answer("тут буде інформація..")


@router.message(Text("Обрати тариф"))
async def choose_tariff(message: Message, state: FSMContext):
    
    # check price block #
    
    await state.set_state(DB.price)
    await message.answer(
        "Яка ціна вас задовільняє?")


@router.message(DB.price)
async def internet_signal(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(
        text="Інтернет",
        callback_data="internet"
    ))

    builder.add(InlineKeyboardButton(
        text="Хвилини",
        callback_data="minutes"
    ))


    await message.answer(
        "Що для вас в пріоритеті, мобільний інтернет чи хвилини?",
        reply_markup=builder.as_markup()
    )
    await state.clear()


@router.callback_query(Text("internet"))
async def internet(callback: CallbackQuery):
    if callback.message is None:
        return

    await callback.message.answer('Яка кількість ГБ Вас задовольнить?')\

    # TODO: add_inline_buttons
    await callback.answer()

@router.callback_query(Text("minutes"))
async def minutes(callback: CallbackQuery):
    if callback.message is None:
        return

    await callback.message.answer('Яка кількість хвилин Вас задовольнить?')

    # TODO: add_inline_buttons
    await callback.answer()
