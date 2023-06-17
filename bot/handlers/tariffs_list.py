from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.bot import bot
from bot.data_provider import data_provider
from bot.formatting.format_list_item import format_list_item


def get_tariffs_list_markup():
    builder = InlineKeyboardBuilder()
    
    builder.add(InlineKeyboardButton(
        text="<<",
        callback_data="list_prev"
    ))

    builder.add(InlineKeyboardButton(
        text=">>",
        callback_data="list_next"
    ))

    return builder.as_markup()

router = Router()
STARTING_INDEX = 0

@router.message(Text("Всі тарифи"))
async def all_tariffs(message: Message, state: FSMContext):
    await state.update_data(tariff_index=STARTING_INDEX)

    tariffs_data = await data_provider.get_tariffs_overview()
    formatted_data = format_list_item(
        STARTING_INDEX + 1,
        len(tariffs_data),
        tariffs_data[STARTING_INDEX]
    )
    
    markup = get_tariffs_list_markup()

    await message.answer(
        text=formatted_data,
        reply_markup=markup
    )


@router.callback_query(Text(startswith="list"))
async def act(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()  
    tariffs_data = await data_provider.get_tariffs_overview()

    old_index = state_data['tariff_index']

    action = callback.data.split('_')[-1]
    new_index = old_index + 1 if action == 'next' else old_index - 1

    await state.update_data(tariff_index=new_index)
    markup = get_tariffs_list_markup()
    formatted_data = format_list_item(
        new_index,
        len(tariffs_data),
        tariffs_data[new_index]
    )

    await bot.edit_message_text(
        text=formatted_data,
        message_id=callback.message.message_id,
        chat_id=callback.message.chat.id,
        reply_markup=markup
    )
