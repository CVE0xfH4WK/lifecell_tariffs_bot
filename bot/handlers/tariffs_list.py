from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.bot import bot
from bot.data_provider import data_provider
from bot.formatting.format_list_item import format_list_item
from bot.messages import DETAILED_INFORMATION, MORE_INFO, SOMETHING_WENT_WRONG
from data import GeneralTariffInfo

LIFECELL_LINK = 'https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/'

def get_tariffs_list_markup(data: GeneralTariffInfo) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.add(InlineKeyboardButton(
        text="<<",
        callback_data="list_prev"
    ))

    builder.add(InlineKeyboardButton(
        text=">>",
        callback_data="list_next"
    ))

    builder.add(InlineKeyboardButton(
        text=DETAILED_INFORMATION,
        url=data.details_page_link
    ))

    builder.add(InlineKeyboardButton(
        text=MORE_INFO,
        url=LIFECELL_LINK
    ))

    builder.adjust(2, 1, 1)
    return builder.as_markup()

router = Router()
STARTING_INDEX = 0

@router.message(Text("Всі тарифи"))
async def all_tariffs(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()

    await state.update_data(tariff_index=STARTING_INDEX)

    tariffs_data = await data_provider.get_tariffs_overview()
    if tariffs_data is None:
        await message.reply(SOMETHING_WENT_WRONG)
        return

    selected_data = tariffs_data[STARTING_INDEX]
    formatted_data = format_list_item(
        STARTING_INDEX + 1,
        len(tariffs_data),
        tariffs_data[STARTING_INDEX]
    )
    
    markup = get_tariffs_list_markup(selected_data)

    await message.answer(
        text=formatted_data,
        reply_markup=markup
    )


@router.callback_query(Text(startswith="list"))
async def act(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()  
    tariffs_data = await data_provider.get_tariffs_overview()

    if tariffs_data is None or callback.data is None:
        await callback.answer()
        return

    action = callback.data.split('_')[-1]

    if 'tariff_index' not in state_data:
        await state.update_data(tariff_index=STARTING_INDEX)
        state_data = await state.get_data()

    old_index = state_data['tariff_index']
    new_index = state_data['tariff_index']

    if action == 'next':
        if new_index + 1 < len(tariffs_data):
            new_index += 1 
    if action == 'prev':
        if new_index - 1 >= 0:
            new_index -= 1

    await state.update_data(tariff_index=new_index)

    new_item = tariffs_data[new_index]
    markup = get_tariffs_list_markup(new_item)

    formatted_data = format_list_item(
        new_index + 1,
        len(tariffs_data),
        new_item
    )

    if callback.message is None:
        await callback.answer()
        return

    if old_index == new_index:
        await callback.answer(text='Більше тарифів немає...')
        return

    await bot.edit_message_text(
        text=formatted_data,
        message_id=callback.message.message_id,
        chat_id=callback.message.chat.id,
        reply_markup=markup
    )
