from datetime import datetime

from core.db.db import connection
from core.db.product import get_products_for_cart
from core.db.user import get_or_create_tguser


@connection
async def create_order(db, cart_products: dict, tguser_id: int, order: dict):
    products_in_cart = await get_products_for_cart(
        [product_id for product_id in cart_products.keys()]
    )
    for product in products_in_cart:
        if cart_products[product['id']] > product['quantity']:
            return (
                f'Упс кажется товар {product["title"]} '
                f'закончился попробуйте оформить заказ еще раз'
            )
    user = await get_or_create_tguser(tg_id=tguser_id)
    cursor = await db.execute(
        'INSERT INTO '
        'goods_order (customer_id, city_id, shipping_address, order_date, phone, customer_name )'
        'VALUES (?, ?, ?, ?, ?, ?)',
        (
            user[0]['id'], order['city'][0],
            order['address'], datetime.now(), order['phone'], order['name']
        )
    )
    products = [('Продукт', 'Кол-во', 'Сумма')]
    for product in products_in_cart:
        cart_quantity = cart_products[product['id']]
        product_id = product['id']
        await db.execute(
            'INSERT INTO '
            'goods_orderitem (order_id, product_id, quantity_ordered, total_price)'
            'VALUES (?, ?, ?, ?)',
            (cursor.lastrowid, product_id, cart_quantity, cart_quantity * product['price'])
        )
        await db.execute(
            "UPDATE goods_product "
            "SET quantity = quantity - ? "
            "WHERE id = ?", (cart_quantity, product_id)
        )
        products.append(
            (product['title'], cart_quantity, cart_quantity * product['price'])
        )
    return products
