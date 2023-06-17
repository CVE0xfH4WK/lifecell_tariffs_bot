from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message

router = Router()

@router.message(Text("Про нас"))
async def info(message: Message):
    await message.answer(
        "Lifecell - ваш надійний партнер у світі зв'язку. " 
        "Обирайте нас і отримайте високоякісні послуги та індивідуальний підхід до вашого зв'язку.")