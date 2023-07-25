from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Update, CallbackQuery

from core.db.product import get_products_for_cart
from core.filters import IsPrivate
from core.keyboards import menu_keyboard
from core.keyboards.order_keyboard import create_order_keyboard
from core.services.common_services import process_sent_messages
from core.services.product import send_product_messages
from core.states import FormOrderContext

router = Router()
router.message.filter(IsPrivate())

CART_PRODUCTS = '🛒️ Товары в корзине'
EMPTY_CART = '🛒 Ваша корзина пуста 😢\nДобавьте товары из каталога'
ORDER = "Оформить заказ"


@router.message(F.text == menu_keyboard.CART)
@router.callback_query(F.data == 'cancel_cart', StateFilter(FormOrderContext))
async def process_show_cart_products(update: Update, state: FSMContext):
    message = update
    if isinstance(update, CallbackQuery):
        message = update.message
    data = await state.get_data()
    bot = message.get_mounted_bot()
    await process_sent_messages(state=state, bot=bot)
    products = await get_products_for_cart(tuple(data.get('cart', dict()).keys()))
    if not products:
        await message.answer(text=EMPTY_CART)
        return
    await message.answer(text=CART_PRODUCTS)
    sent_products_messages = await send_product_messages(
        products=products, update=message, state=state
    )
    if sent_products_messages:
        form_order_message = await message.answer(text=ORDER, reply_markup=create_order_keyboard())
        await state.update_data(
            sent_form_order_message=(form_order_message.chat.id, form_order_message.message_id)
        )
    await state.update_data(sent_products_messages=sent_products_messages)
    await state.set_state()

