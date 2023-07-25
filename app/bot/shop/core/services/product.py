import asyncio

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from core.utils.cart import update_cart
from core.utils.product import create_product_message


async def send_product_messages(update: CallbackQuery | Message, state: FSMContext, products: list):
    data = await state.get_data()
    cart_data = data.get('cart', dict())
    sent_messages = []
    message = update
    if isinstance(update, CallbackQuery):
        message = update.message
    for product in products:
        product_message = await create_product_message(product=product, cart=cart_data)
        product_message = await message.answer_photo(**product_message)
        await asyncio.sleep(1)
        await update_cart(product=product, state=state, action='check')
        sent_messages.append((product_message.chat.id, product_message.message_id))
    return sent_messages


async def remove_sent_product_keyboards_if_exists(data: dict, bot: Bot):
    for sent_message in data.get('sent_products_messages', ()):
        # Пытаемся убрать клавиатуры у отправленных пользователю продуктах
        try:
            await bot.edit_message_reply_markup(*sent_message, reply_markup=None)
        except TelegramBadRequest:
            continue


async def edit_product_message(
    callback_query: CallbackQuery, product: dict, cart: dict
):
    try:
        product_message = await create_product_message(product=product, cart=cart)
        await callback_query.message.edit_caption(**product_message)
    except TelegramBadRequest:
        await callback_query.answer()
