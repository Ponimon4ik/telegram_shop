from datetime import datetime

from aiogram import F, Router
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, Update

from core.db.order import create_order
from core.filters import IsPrivate
from core.keyboards.order_keyboard import (
    create_cities_keyboard, create_cancel_keyboard, create_accord_keyboard
)
from core.services.common_services import process_sent_messages
from core.services.order import update_order
from core.states import FormOrderContext
from core.utils.order import get_description_order, create_exel

router = Router()
router.message.filter(IsPrivate())


CHOOSE_CITY = 'Выберите город'
TYPE_ADDRESS = 'Введите ваш адрес в формате: Улица Дом/Корпус Квартира'
TYPE_NAME = 'Введите Ваше имя, как я могу к Вам обращаться ?'
TYPE_PHONE = 'Введите номер телефона для связи с Вами'
ACCORD = 'Город: {0}\nАдрес: {1}\n Имя: {2}\n Телефон: {3}\n\n'


@router.callback_query(F.data == 'cancel_exit')
async def process_select_city(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await state.update_data(order={})
    await state.set_state()


@router.callback_query(F.data.in_(('order', 'cancel_city')))
async def process_select_city(callback_query: CallbackQuery, state: FSMContext):
    cities = [
        {'id': 1, 'name': 'Москва'},
        {'id': 2, 'name': 'С.Петербург'}
    ]
    if callback_query.data == 'cancel_city':
        await state.update_data(order={})
        await callback_query.message.edit_text(
            text=CHOOSE_CITY, reply_markup=create_cities_keyboard(cities)
        )
    else:
        await process_sent_messages(state=state, bot=callback_query.get_mounted_bot())
        await callback_query.message.answer(
            text=CHOOSE_CITY, reply_markup=create_cities_keyboard(cities)
        )
    await state.set_state(FormOrderContext.get_city)


@router.callback_query(F.data.startswith(('city', 'cancel_address')))
async def process_type_address(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data != 'cancel_address':
        _, city_id, city_name = callback_query.data.split(':')
        await update_order(state=state, data=('city', (city_id, city_name)))
    address_message = await callback_query.message.edit_text(
        text=TYPE_ADDRESS, reply_markup=create_cancel_keyboard('city')
    )
    await state.update_data(address_message=(address_message.chat.id, address_message.message_id))
    await state.set_state(FormOrderContext.get_address)


@router.callback_query(F.data == 'cancel_name')
@router.message(StateFilter(FormOrderContext.get_address), F.content_type == ContentType.TEXT)
async def process_type_name(update: Update, state: FSMContext):
    if isinstance(update, CallbackQuery):
        name_message = await update.message.edit_text(
            text=TYPE_NAME, reply_markup=create_cancel_keyboard('address')
        )
    else:
        await update_order(state=state, data=('address', update.text))
        await process_sent_messages(state=state, bot=update.get_mounted_bot())
        name_message = await update.answer(
            text=TYPE_NAME, reply_markup=create_cancel_keyboard('address')
        )
    await state.update_data(name_message=(name_message.chat.id, name_message.message_id))
    await state.set_state(FormOrderContext.get_name)


@router.callback_query(F.data == 'cancel_phone')
@router.message(StateFilter(FormOrderContext.get_name), F.content_type == ContentType.TEXT)
async def process_type_phone(update: Update, state: FSMContext):
    if not isinstance(update, Message):
        phone_message = await update.message.edit_text(
            text=TYPE_PHONE, reply_markup=create_cancel_keyboard('name')
        )
    else:
        await update_order(state=state, data=('name', update.text))
        await process_sent_messages(state=state, bot=update.get_mounted_bot())
        phone_message = await update.answer(
            text=TYPE_PHONE, reply_markup=create_cancel_keyboard('name')
        )
    await state.update_data(phone_message=(phone_message.chat.id, phone_message.message_id))
    await state.set_state(FormOrderContext.get_phone)


@router.message(StateFilter(FormOrderContext.get_phone), F.content_type == ContentType.TEXT)
async def process_get_accord(message: Message, state: FSMContext):
    updated_order = await update_order(state=state, data=('phone', message.text))
    await process_sent_messages(state=state, bot=message.get_mounted_bot())
    await message.answer(
        text=ACCORD.format(*get_description_order(updated_order)),
        reply_markup=create_accord_keyboard()
    )
    await state.set_state(FormOrderContext.get_accord)


@router.callback_query(F.data == 'accord')
async def process_accord(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cart = data.get('cart', {})
    order = data.get('order', {})
    formed_products_order = await create_order(
        cart_products=cart,
        tguser_id=callback_query.message.from_user.id,
        order=order
    )
    if isinstance(formed_products_order, str):
        await callback_query.message.edit_text(text=formed_products_order)
        return
    file_name = f'{datetime.now()}'
    create_exel(
        file_name=file_name,
        product_data=formed_products_order,
        order_data=(('Город', 'Адрес', 'Имя', 'Телефон'), get_description_order(order)))
    await callback_query.message.edit_text(
        text='Ваш заказ сформирован!'
    )
    await state.clear()
