from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.filters import IsPrivate
from core.keyboards.product_keyboard import ProductCallbackFactory
from core.services.product import send_product_messages, edit_product_message
from core.utils.cart import update_cart
from core.db.product import get_products_for_subcategory, get_product


EMPTY_SUBCATEGORY = 'Упс, кажется товары в этой категории уже закончились'
PRODUCT_NO_EXIST = 'Упс, кажется товара больше не существует'
SUBCATEGORY_TITLE = '🛍️ {subcategory_title}'

router = Router()
router.message.filter(IsPrivate())


@router.callback_query(F.data.startswith('subcategory'))
async def process_show_products(callback_query: CallbackQuery, state: FSMContext):
    _, subcategory_id = callback_query.data.split('_')
    # Больше не храним данные об отправленном каталоге.
    # Пользователь закончил с ним работу и должен получить список продуктов
    await state.update_data(sent_categories_message=None)  # todo не нравится
    data = await state.get_data()
    products = await get_products_for_subcategory(
        subcategory_id=subcategory_id,
        cart_products_ids=list(data.get('cart', dict()).keys())
    )
    if not products:
        await callback_query.message.edit_text(text=EMPTY_SUBCATEGORY, reply_markup=None)
        return
    # Удаляем инлайн меню
    await callback_query.message.delete()
    await callback_query.message.answer(
        text=SUBCATEGORY_TITLE.format(subcategory_title=products[0]['subcategory_title'])
    )
    sent_products_messages = await send_product_messages(
        products=products, update=callback_query, state=state
    )
    await state.update_data(sent_products_messages=sent_products_messages)


@router.callback_query(ProductCallbackFactory.filter())
async def process_select_product(callback_query: CallbackQuery, state: FSMContext):
    _, product_id, action = callback_query.data.split('_')
    product_id = int(product_id)
    product = await get_product(product_id)
    if not product:
        await callback_query.message.edit_text(text=PRODUCT_NO_EXIST, reply_markup=None)
        return
    updated_cart = await update_cart(product=product, action=action, state=state)
    if product['quantity'] <= 0 and action == 'clean':
        await callback_query.message.delete()
        return
    await edit_product_message(
        callback_query=callback_query, product=product, cart=updated_cart
    )
