from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

FORM_ORDER = "Перейти к оформлению"

BACK_TO_CART = '🔙 Вернуться в корзину'
BACK_TO_CITY = '🔙 Вернуться к выбору города'
BACK_TO_ADDRESS = '🔙 Вернуться к заполнению адреса'
BACK_TO_NAME = '🔙 Вернуться к заполнению имени'
BACK_TO_PHONE = '🔙 Вернуться к заполнению телефона'
CANCEL_ORDER = '🛑 Отменить оформление заказа'
ACCORD_ORDER = '✅ Подтвердить'
PAY = 'Оплатить'


class CancelCallbackFactory(CallbackData, prefix='cancel', sep='_'):
    back_to: str


buttons = {
    'cart': InlineKeyboardButton(
        text=BACK_TO_CART, callback_data=CancelCallbackFactory(back_to='cart').pack()
    ),
    'city': InlineKeyboardButton(
        text=BACK_TO_CITY, callback_data=CancelCallbackFactory(back_to='city').pack()
    ),
    'address': InlineKeyboardButton(
        text=BACK_TO_ADDRESS, callback_data=CancelCallbackFactory(back_to='address').pack()
    ),
    'name': InlineKeyboardButton(
        text=BACK_TO_NAME, callback_data=CancelCallbackFactory(back_to='name').pack()
    ),
    'phone': InlineKeyboardButton(
        text=BACK_TO_PHONE, callback_data=CancelCallbackFactory(back_to='phone').pack()
    ),
    'exit': InlineKeyboardButton(
        text=CANCEL_ORDER, callback_data=CancelCallbackFactory(back_to='exit').pack()
    ),
}


def create_order_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    button = InlineKeyboardButton(text=FORM_ORDER, callback_data='order')
    kb.add(button)
    return kb.as_markup()


def create_cities_keyboard(cities: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        *[
            InlineKeyboardButton(text=city['name'],
                                 callback_data=f'city:{city["id"]}:{city["name"]}') for
            city in cities
        ],
        width=2
    )
    kb.row(buttons['cart'], width=1)
    kb.row(buttons['exit'], width=1)
    return kb.as_markup()


def create_cancel_keyboard(back_to: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(buttons[back_to], width=1)
    kb.row(buttons['exit'], width=1)
    return kb.as_markup()


def create_accord_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=ACCORD_ORDER, callback_data='accord'))
    kb.row(buttons['phone'], width=1)
    kb.row(buttons['exit'], width=1)
    return kb.as_markup()
