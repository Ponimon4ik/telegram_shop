from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


CATALOG = '🛍️ Каталог'
CART = '🛒 Корзина'
FAQ = '❓ FAQ'

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=CART), KeyboardButton(text=CATALOG)],
        [KeyboardButton(text=FAQ)]
    ],
    resize_keyboard=True,
)
