from aiogram import F, Router
from aiogram.types import Message

from core.filters import IsPrivate
from core.keyboards import menu_keyboard

router = Router()
router.message.filter(IsPrivate())


@router.message(F.text == menu_keyboard.FAQ)
async def process_catalog(message: Message):
    await message.answer(text='Faq')