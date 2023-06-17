from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (CallbackQuery, InlineKeyboardButton, KeyboardButton,
                           ReplyKeyboardRemove, Message)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


mob_data_volume = [
    1, 10, 25,
    "безліміт"
]

minutes_volume = [
    10, 20, 30,
    "безліміт"
]


class DB(StatesGroup):
    price = State()
    internent_minutes_prio = State()
    internent_minutes = State()
    sms = State()
    rouming = State()


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
        "Яка ціна вас задовольняє?",
        reply_markup=ReplyKeyboardRemove())


@router.message(DB.price)
async def internet_signal(message: Message, state: FSMContext):
    # write price data

    await state.set_state(DB.internent_minutes_prio)
    await state.update_data(price=message.text)
    
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(
        text="Інтернет",
        callback_data="act_internet"
    ))

    builder.add(InlineKeyboardButton(
        text="Хвилини",
        callback_data="act_minutes"
    ))


    await message.answer(
        "Що для вас в пріоритеті, гігабайти чи хвилини?",
        reply_markup=builder.as_markup()
    )

@router.callback_query(Text(startswith="act_"))
async def minutes(callback: CallbackQuery, state: FSMContext):
    # write action data

    await state.set_state(DB.internent_minutes)
    await state.update_data(internet_minutes_prio=callback.data)

    builder = InlineKeyboardBuilder()
    builder.adjust(2)
    
    if callback.data.split("_")[1] == "internet":
        if callback.message is None:
            return

        for data in mob_data_volume:
            builder.add(InlineKeyboardButton(
                text=f"{data} ГБ",
                callback_data=f"gb_{data}"
            ))


        await callback.message.answer(
            'Яка кількість гігабайт вас задовольнить?',
            reply_markup=builder.as_markup())

        await callback.answer()
    
    
    if callback.data.split("_")[1] == "minutes":
        if callback.message is None:
            return

        for data in minutes_volume:
            builder.add(InlineKeyboardButton(
                text=f"{data} хв.",
                callback_data=f"mins_{data}"
            ))


        await callback.message.answer(
            'Яка кількість хвилин вас задовольнить?',
            reply_markup=builder.as_markup())

        await callback.answer()


@router.callback_query(Text(startswith=["mins_", "gb_"]))
async def sms(callback: CallbackQuery, state: FSMContext):
    # write mins/gb data
    await state.set_state(DB.sms)
    await state.update_data(internet_minutes=callback.data)

    builder = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(
            text="ніколи",
            callback_data="sms_never"
        ),
        InlineKeyboardButton(
            text="рідко",
            callback_data="sms_seldome"
        ),
        InlineKeyboardButton(
            text="часто",
            callback_data="sms_often"
        ),
        InlineKeyboardButton(
            text="дуже часто",
            callback_data="sms_veryOften"
        )
    ]

    for button in buttons:
        builder.add(button)

    await callback.message.answer(
        'Як часто ви користуєтесь SMS повідомленнями?',
        reply_markup=builder.as_markup()
    )

    await callback.answer()
    


@router.callback_query(Text(startswith="sms_"))
async def rouming(callback: CallbackQuery, state: FSMContext):
    # write sms data
    await state.set_state(DB.rouming)
    await state.update_data(sms=callback.data)

    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="Так",
            callback_data="roum_true"
        )
    )

    builder.add(
        InlineKeyboardButton(
            text="Ні",
            callback_data="roum_false"
        )
    )

    await callback.message.answer(
        text="Чи часто ви перебуваєте за кордоном?" 
        "(це допоможе нам дізнатись чи потрібен вам роумінг)",
        reply_markup=builder.as_markup()
    )

    


@router.callback_query(Text(startswith="roum_"))
async def output_tariff(callback: CallbackQuery, state: FSMContext):
    # write rouming data

    await state.update_data(rouming=callback.data)

    # choose tariff

    
    data = await state.get_data()
    await state.clear()
    #await callback.message.answer("тут буде підібраний тариф..")
    await callback.message.answer(f"DATA: {data}")
