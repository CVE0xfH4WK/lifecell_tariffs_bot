from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.methods.edit_message_text import EditMessageText
from aiogram.types import (CallbackQuery, InlineKeyboardButton, KeyboardButton,
                           ReplyKeyboardRemove, Message)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


from bot.handlers.bot import bot


mob_data_volume = [
    1, 10, 
    20, "безліміт"
]

minutes_volume = [
    10, 20, 
    30, "безліміт"
]


tariffs = [
    "tariff 1",
    "tariff 2",
    "tariff 3",
]


class DB(StatesGroup):
    price = State()
    internent_minutes_prio = State()
    internent_minutes = State()
    sms = State()
    rouming = State()


class MenuState(StatesGroup):
    main = State()
    tariffs_list = State()


router = Router()


@router.message(Command(commands=["start"]))
async def start(message: Message):
    buttons = [
        "Про нас", "Всі тарифи",
        "Обрати тариф"
    ]

    builder = ReplyKeyboardBuilder()
    for button in buttons:
        builder.add(KeyboardButton(text=button))
    builder.adjust(2)


    await message.answer(f"Вітаю, {message.from_user.first_name}.\n"
                         f"\nЯ - Lifecell Bot, офіційний бот компанії-оператора Lifecell."
                         f"\nОберіть дію, для того, щоб продорвжити : ",
                         reply_markup=builder.as_markup(resize_keyboard=True))


@router.message(Text("Про нас"))
async def info(message: Message):
    await message.answer(
        "Lifecell - ваш надійний партнер у світі зв'язку. " 
        "Обирайте нас і отримайте високоякісні послуги та індивідуальний підхід до вашого зв'язку.")

@router.message(Text("Всі тарифи"))
async def all_tariffs(message: Message, state: FSMContext):

    await state.set_state(MenuState.main)
    await state.update_data(main=0)

    await state.set_state(MenuState.tariffs_list)
    await state.update_data(tariffs_list=tariffs)
    
    data = await state.get_data()

    builder = InlineKeyboardBuilder()
    
    builder.add(InlineKeyboardButton(
        text="<<",
        callback_data="actionBackward"
    ))

    builder.add(InlineKeyboardButton(
        text="Обрати",
        callback_data="actionChoose"
    ))

    builder.add(InlineKeyboardButton(
        text=">>",
        callback_data="actionForward"
    ))

    await message.answer(tariffs[0], reply_markup=builder.as_markup())
    

@router.callback_query(Text(startswith="action"))
async def act(callback: CallbackQuery, state: FSMContext):
    
    data = await state.get_data()  

    builder = InlineKeyboardBuilder()
    
    builder.add(InlineKeyboardButton(
        text="<<",
        callback_data="actionBackward"
    ))

    builder.add(InlineKeyboardButton(
        text="Обрати",
        callback_data="actionChoose"
    ))

    builder.add(InlineKeyboardButton(
        text=">>",
        callback_data="actionForward"
    ))


    if callback.data == 'actionBackward':
        await state.update_data(main=data['main']-1)

        await bot.edit_message_text(
            text=data['tariffs_list'][data['main']-1],
            message_id=callback.message.message_id,
            chat_id=callback.message.chat.id,
            reply_markup=builder.as_markup()
            )
        

    elif callback.data == 'actionChoose':
        await callback.message.answer(f"Ви обрали {data['tariffs_list'][data['main']]}")

    elif callback.data == 'actionForward':
        await state.update_data(main=data['main']+1)
        
        await bot.edit_message_text(
            text=data['tariffs_list'][data['main']+1],
            message_id=callback.message.message_id,
            chat_id=callback.message.chat.id,
            reply_markup=builder.as_markup()
            )


@router.message(Text("Обрати тариф"))
async def choose_tariff(message: Message, state: FSMContext):
    
    # check price block #
    
    await state.set_state(DB.price)
    await message.answer(
        "Яка ціна вас задовольняє?",
        reply_markup=ReplyKeyboardRemove(remove_keyboard=True))


@router.message(DB.price)
async def internet_signal(message: Message, state: FSMContext):
    await state.set_state(DB.internent_minutes_prio)
    await state.update_data(price=message.text)
    
    builder = InlineKeyboardBuilder()
    builder.adjust(2)

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
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

@router.callback_query(Text(startswith="act_"))
async def minutes(callback: CallbackQuery, state: FSMContext):
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
            reply_markup=builder.as_markup(resize_keyboard=True))

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
            reply_markup=builder.as_markup(resize_keyboard=True))

        await callback.answer()


@router.callback_query(Text(startswith=["mins_", "gb_"]))
async def sms(callback: CallbackQuery, state: FSMContext):
    await state.set_state(DB.sms)
    await state.update_data(internet_minutes=callback.data)

    builder = InlineKeyboardBuilder()
    builder.adjust(2)

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
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

    await callback.answer()
    

@router.callback_query(Text(startswith="sms_"))
async def rouming(callback: CallbackQuery, state: FSMContext):
    await state.set_state(DB.rouming)
    await state.update_data(sms=callback.data)

    builder = InlineKeyboardBuilder()
    builder.adjust(2)

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
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

    
@router.callback_query(Text(startswith="roum_"))
async def output_tariff(callback: CallbackQuery, state: FSMContext):
    await state.update_data(rouming=callback.data)

    # choose tariff
    
    data = await state.get_data()
    await state.clear()

    await callback.message.answer(f"DATA: {data}")
