from collections import defaultdict

from aiogram.fsm.context import FSMContext


async def update_cart(product: dict, state: FSMContext, action: str):
    product_id = product['id']
    data = await state.get_data()
    cart_data = defaultdict(int, data.get('cart', dict()))
    if action == 'check':
        if product['quantity'] < cart_data[product_id]:
            cart_data[product_id] = product['quantity']
        elif cart_data[product_id] <= 0:
            cart_data.pop(product_id, None)
    elif action == 'add':
        if cart_data[product_id] < product['quantity']:
            cart_data[product_id] += 1
    elif cart_data[product_id] <= 0 or action == 'clean':
        cart_data.pop(product_id, None)
    elif product['quantity'] < cart_data[product_id]:
        difference = cart_data[product_id] - product['quantity']
        cart_data[product_id] -= difference + 1
    else:
        cart_data[product_id] -= 1
    await state.update_data(cart=dict(cart_data))
    return cart_data
