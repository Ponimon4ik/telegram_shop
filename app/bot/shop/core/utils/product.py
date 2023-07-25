from pathlib import Path

from aiogram.types import FSInputFile

from core.keyboards.product_keyboard import create_product_keyboard

PRICE = '\nЦена за единицу: {0}₽'
STOCK_QUANTITY = '\nКоличество на складе: {0}шт.'
IN_CART = '\n✅ В корзине: '
TOTAL_PRICE = '\n⚠️ Сумма {0}₽'
PRODUCT_IS_OVER = '\n🚫 К сожалению данный товар только что закончился 😢'
LESS_STOCK = (
    '\n\n❗️ Обратите внимание ❗'
    '\nТовара на складе стало меньше.'
    '\nКоличество в корзине обновлено до {}шт.'
)

MEDIA_PATH = Path('media')


def get_product_caption(product: dict, cart_product_quantity: int, ) -> str:
    def _get_description_in_cart(quantity: int, product_price: int) -> str:
        return IN_CART + str(quantity) + TOTAL_PRICE.format(product_price * quantity)
    price = product['price']
    stock_quantity = product['quantity'] if product['quantity'] >= 0 else 0
    in_cart_message = _get_description_in_cart(cart_product_quantity, price)
    if cart_product_quantity <= 0:
        in_cart_message = ''
    if stock_quantity <= 0:
        in_cart_message = PRODUCT_IS_OVER
    elif stock_quantity < cart_product_quantity:
        in_cart_message = _get_description_in_cart(stock_quantity, price) + LESS_STOCK.format(stock_quantity)
    return (
        product['title'] + '\n' + product['description'] +
        PRICE.format(price) + STOCK_QUANTITY.format(stock_quantity) + in_cart_message
    )


async def create_product_message(product: dict, cart: dict) -> dict:
    picture = Path('media') / product['picture']
    cart_product_quantity = cart.get(product['id'], 0)
    return {
        'photo': FSInputFile(picture),
        'caption': get_product_caption(
            cart_product_quantity=cart_product_quantity, product=product),
        'reply_markup': create_product_keyboard(
            product_id=product['id'], cart_product_quantity=cart_product_quantity,
            price=product['price'], stock_product_quantity=product['quantity']
        )
    }






