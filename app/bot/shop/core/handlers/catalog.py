from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Update

from core.filters import IsPrivate
from core.keyboards import menu_keyboard

from core.services.catalog import (
    send_categories_or_change_to_categories, change_categories_to_subcategories, send_new_page,
)
from core.services.common_services import process_sent_messages

router = Router()
router.message.filter(IsPrivate())


@router.callback_query(F.data == 'category')
@router.message(F.text == menu_keyboard.CATALOG)
async def process_show_catalog(update: Update, state: FSMContext):
    bot = update.get_mounted_bot()
    await process_sent_messages(state=state, bot=bot)
    message = await send_categories_or_change_to_categories(update=update)
    if message:
        # Обновляем в хранилище данные об отправленном каталоге
        await state.update_data(sent_categories_message=(message.chat.id, message.message_id))
    # Перестаем следить за category_id, т.к. пользователь находится в состоянии выбора категории
    await state.update_data(category_id=None)


@router.callback_query(F.data.startswith('category'))
async def process_show_subcategories(callback_query: CallbackQuery, state: FSMContext):
    _, category_id = callback_query.data.split('_')
    # Запоминаем ид категории для пагинации подкатегорий
    await state.update_data(category_id=category_id)
    await change_categories_to_subcategories(
        callback_query=callback_query, category_id=int(category_id)
    )


@router.callback_query(F.data.startswith(('next', 'prev')))
async def process_pagination(callback_query: CallbackQuery, state: FSMContext):
    action, from_page = callback_query.data.split('_')
    page = {
        'next': int(from_page) + 1,
        'prev': int(from_page) - 1
    }
    data = await state.get_data()
    await send_new_page(
        callback_query=callback_query, category_id=data.get('category_id', None),
        number_page=page[action]
    )
