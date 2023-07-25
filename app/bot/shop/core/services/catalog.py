from aiogram.types import Update, Message, CallbackQuery

from core.db.catalog import get_all_categories, get_subcategories_for_category
from core.utils.catalog import create_catalog_message


async def send_categories_or_change_to_categories(update: Update):
    categories = await get_all_categories()
    if isinstance(update, Message):
        # Отправляем новый каталог
        message = await update.answer(**create_catalog_message(categories))
        return message
    # Пользователь нажал на кнопку вернуться в каталог из подкатегорий.
    # Возвращаем каталог с категориями
    await update.message.edit_text(**create_catalog_message(categories))
    await update.answer()


async def change_categories_to_subcategories(
    callback_query: CallbackQuery, category_id: int,
):
    subcategories = await get_subcategories_for_category(category_id=int(category_id))
    await callback_query.message.edit_text(
        **create_catalog_message(categories=subcategories, is_subcategory=True)
    )
    await callback_query.answer()


async def send_new_page(callback_query:CallbackQuery, category_id: int | None, number_page: int):
    # Если есть category_id значит пользователь в подкатегориях
    if category_id:
        is_subcategory = True
        categories = await get_subcategories_for_category(category_id=int(category_id))
    else:
        is_subcategory = False
        categories = await get_all_categories()
    await callback_query.message.edit_text(
        **create_catalog_message(
            categories=categories, is_subcategory=is_subcategory, current_page=number_page)
    )
    await callback_query.answer()
