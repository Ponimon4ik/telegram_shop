from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from core.services.product import remove_sent_product_keyboards_if_exists


async def process_sent_messages(state: FSMContext, bot: Bot):
    data = await state.get_data()
    await remove_sent_product_keyboards_if_exists(data=data, bot=bot)
    await state.update_data(sent_products_messages=())
    for sent_message in (
        'sent_categories_message', 'sent_form_order_message', 'address_message',
        'name_message', 'phone_message'
    ):
        message = data.get(sent_message, None)
        if message:
            try:
                await bot.delete_message(*message)
            except TelegramBadRequest:
                pass
            await state.update_data(**{sent_message: None})
