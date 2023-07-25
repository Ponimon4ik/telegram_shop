from aiogram.fsm.context import FSMContext


async def update_order(state: FSMContext, data: tuple):
    key, value = data
    data = await state.get_data()
    order = data.get('order', {})
    order[key] = value
    await state.update_data(order=order)
    return order
