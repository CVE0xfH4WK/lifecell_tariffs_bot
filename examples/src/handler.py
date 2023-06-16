import asyncio

from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup 
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup


from src.question_logics import Checker


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
        text=f"Інтернет",
        callback_data=f"internet"
    ))

    builder.add(InlineKeyboardButton(
        text=f"Хвилини",
        callback_data=f"minutes"
    ))


    await message.answer(
        "Що для вас в пріорететі, мобільний інтернет чи хвилини?",
        reply_markup=builder.as_markup()
    )


@router.callback_query(Text("internet"))
async def internet(callback: CallbackQuery):
    await callback.message.answer('Яка кількість гб Вас задовольнить?')\
    #add_inline_buttons
    await callback.answer()

@router.callback_query(Text("minutes"))
async def internet(callback: CallbackQuery):
    await callback.message.answer('Яка кількість хвилин Вас задовольнить?')
    #add_inline_buttons
    await callback.answer()
'''
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
'''


#@router.callback_query(Text(""))
#async def 
