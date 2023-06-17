import re
from typing import Literal, cast

from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.bot import bot
from bot.formatting.format_general_overview import format_general_overview
from bot.handlers.about_us import router as about_us_router
from bot.handlers.start import router as start_router
from bot.handlers.tariffs_list import router as tariffs_list_router
from bot.logics import VALUES_DATASET, UserData, closest_value, pick_tariffs
from bot.messages import (COULD_NOT_PICK, DETAILED_INFORMATION,
                          MESSAGE_WAS_DELETED, SOMETHING_WENT_WRONG)


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
    
    await state.set_state(DB.price)

    await message.answer(
        "Яка ціна тарифу вас задовольняє?"
    )

NO_NUMBER_MESSAGE = 'Будь ласка, пришліть число...'
SINGLE_NUMBER_REGEX = re.compile('[0-9]+')

@router.message(DB.price)
async def internet_signal(message: Message, state: FSMContext):
    await state.set_state(DB.internet_minutes_prio)
    if message.text is None:
        await message.reply(text=NO_NUMBER_MESSAGE)
        return

    numbers = SINGLE_NUMBER_REGEX.findall(message.text)
    if len(numbers) <= 0:
        await message.reply(text=NO_NUMBER_MESSAGE)
        return

    await state.update_data(price=closest_value(VALUES_DATASET['price'], int(message.text)))

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
    if callback.message is None:
        await callback.answer(MESSAGE_WAS_DELETED)
        return

    if callback.data is None:
        await callback.answer(SOMETHING_WENT_WRONG)
        return

    await state.set_state(DB.internet_minutes)
    await state.update_data(internet_minutes_prio=callback.data)

    builder = InlineKeyboardBuilder()

    ActionToHandle = Literal['iternet', 'minutes']
    action_to_handle = cast(
        ActionToHandle,
        callback.data.split('_')[1]
    )

    action_to_labels = {
        'internet': ('gb', VALUES_DATASET['gb']),
        'minutes': ('mins', VALUES_DATASET['min'])
    }

    response_message = None
    if action_to_handle == "internet":
        response_message = 'Яка кількість гігабайт вас задовольнить?'
    elif action_to_handle == 'minutes':
        response_message = 'Яка кількість хвилин вас задовольнить?'


    callback_data_prefix, labels_list = action_to_labels[action_to_handle]
    for button_label in labels_list:
        builder.add(InlineKeyboardButton(
            text=f"{button_label}",
            callback_data=f"{callback_data_prefix}_{button_label}"
        ))

    builder.adjust(3)

    if response_message is None:
        await callback.answer(SOMETHING_WENT_WRONG)
        return

    await callback.message.answer(
        text=response_message,
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

    await callback.answer()


@router.callback_query(Text(startswith=["mins_", "gb_"]))
async def sms(callback: CallbackQuery, state: FSMContext):
    if callback.message is None:
        await callback.answer(MESSAGE_WAS_DELETED)
        return

    await state.set_state(DB.sms)
    await state.update_data(internet_minutes=callback.data)

    builder = InlineKeyboardBuilder()

    button_labels = ["ніколи", "рідко", "часто", "дуже часто"]
    buttons_callback_data = ["sms_never", "sms_seldom", "sms_often", "sms_veryOften"]

    for label, callback_data in zip(button_labels, buttons_callback_data):
        builder.add(InlineKeyboardButton(
            text=label,
            callback_data=callback_data
        ))

    builder.adjust(2)

    await callback.message.answer(
        'Як часто ви користуєтесь SMS повідомленнями?',
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

    await callback.answer()
    

@router.callback_query(Text(startswith="sms_"))
async def roaming(callback: CallbackQuery, state: FSMContext):
    if callback.message is None:
        await callback.answer(MESSAGE_WAS_DELETED)
        return

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
    if callback.message is None:
        await callback.answer(MESSAGE_WAS_DELETED)
        return

    possible_choices = await pick_tariffs(cast(UserData, data))
    if possible_choices is None:
        await callback.answer(COULD_NOT_PICK)
        return

    all_message_data: list[tuple[str, str]] = []
    for choice in possible_choices:
        formatted_message = format_general_overview(choice)
        all_message_data.append((choice.details_page_link, formatted_message))

    for url, text in all_message_data:
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text=DETAILED_INFORMATION,
            url=url
        ))

        await callback.message.reply(
            'Ось тарифи які ми для вас підібрали:'
        )

        await bot.send_message(
            text=text,
            chat_id=callback.message.chat.id,
            reply_markup=builder.as_markup()
        )
