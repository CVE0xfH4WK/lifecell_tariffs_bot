from typing import Literal

from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (CallbackQuery, InlineKeyboardButton, Message,
                           ReplyKeyboardRemove)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.handlers.about_us import router as about_us_router
from bot.handlers.start import router as start_router
from bot.handlers.tariffs_list import router as tariffs_list_router


class DB(StatesGroup):
    price = State()
    internet_minutes_prio = State()
    internet_minutes = State()
    sms = State()
    roaming = State()


router = Router()

# Including additional routers from other files in the bot.handlers
router.include_routers(tariffs_list_router, start_router, about_us_router)


@router.message(Text("Обрати тариф"))
async def choose_tariff(message: Message, state: FSMContext):
    
    # check price block #
    
    await state.set_state(DB.price)
    await message.answer(
        "Яка ціна вас задовольняє?"
    )


@router.message(DB.price)
async def internet_signal(message: Message, state: FSMContext):
    await state.set_state(DB.internet_minutes_prio)
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
    await state.set_state(DB.internet_minutes)
    await state.update_data(internet_minutes_prio=callback.data)

    builder = InlineKeyboardBuilder()
    builder.adjust(2)
    
    if callback.message is None:
        return

    mob_data_volume = [
        1, 10, 
        20, "безліміт"
    ]

    minutes_volume = [
        10, 20, 
        30, "безліміт"
    ]

    action_to_handle: Literal['internet'] | Literal['minutes'] = callback.data.split('_')[1]
    action_to_labels = {
        'internet': mob_data_volume,
        'minutes': minutes_volume
    }

    for button_label in action_to_labels[action_to_handle]:
        builder.add(InlineKeyboardButton(
            text=f"{button_label}",
            callback_data=f"gb_{button_label}"
        ))

    if action_to_handle == "internet":
        response_message = 'Яка кількість гігабайт вас задовольнить?'
    elif action_to_handle == 'minutes':
        response_message = 'Яка кількість хвилин вас задовольнить?'

    await callback.message.answer(
        text=response_message,
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

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
            callback_data="sms_seldom"
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
async def roaming(callback: CallbackQuery, state: FSMContext):
    await state.set_state(DB.roaming)
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
    await state.update_data(roaming=callback.data)
    
    data = await state.get_data()
    print(data)

    await state.clear()

    await callback.message.answer(f"DATA: {data}")
