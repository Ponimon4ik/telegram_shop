from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData


ADD_CART_BUTTON = '✅ Добавить в корзину'
DELETE_FROM_CART_BUTTON = '❌ Убрать из корзины'
INCREASE_BUTTON = '➕'
DECREASE_BUTTON = '➖'


class ProductCallbackFactory(CallbackData, prefix='product', sep='_'):
    id: int
    action: str


def create_product_keyboard(
    product_id: int, cart_product_quantity: int,
    price: int, stock_product_quantity: int
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    callback_data = ProductCallbackFactory(
        id=product_id, action='add'
    )
    add_button = InlineKeyboardButton(
        text=ADD_CART_BUTTON, callback_data=callback_data.pack()
    )
    if stock_product_quantity <= 0:
        callback_data.action = 'clean'
        kb.row(
            InlineKeyboardButton(
                text=DELETE_FROM_CART_BUTTON, callback_data=callback_data.pack()
            )
        )
    elif cart_product_quantity > 0:
        add_button.text = INCREASE_BUTTON
        callback_data.action = 'remove'
        kb.add(InlineKeyboardButton(text=DECREASE_BUTTON, callback_data=callback_data.pack()))
        if stock_product_quantity > cart_product_quantity:
            kb.add(add_button)
        callback_data.action = 'clean'
        kb.row(
            InlineKeyboardButton(
                text=DELETE_FROM_CART_BUTTON, callback_data=callback_data.pack()
            )
        )
    else:
        kb.add(add_button)
    return kb.as_markup()
