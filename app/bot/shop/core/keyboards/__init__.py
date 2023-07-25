from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton

CATALOG = '🛍️ Каталог'
CART = '🛒 Корзина'
FAQ = '❓ FAQ'


keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=CATALOG), KeyboardButton(text=CART)],
        [KeyboardButton(text=FAQ)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
