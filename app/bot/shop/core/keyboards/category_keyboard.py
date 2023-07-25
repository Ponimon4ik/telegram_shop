from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder, InlineKeyboardMarkup

ITEMS_PER_PAGE = 6


def create_catalog_keyboard(page_number, categories, subcategory=False) -> InlineKeyboardMarkup:
    start_index = (page_number - 1) * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    callback_prefix = 'category_' if not subcategory else 'subcategory_'
    if not categories:
        kb_builder.row(InlineKeyboardButton(text="🔙 В категории", callback_data="category"))
        return kb_builder.as_markup()
    kb_builder.row(
        *[
            InlineKeyboardButton(
                text=category['title'],
                callback_data=f'{callback_prefix}{category["id"]}'
            ) for category in categories[start_index:end_index]
        ],
        width=2
    )
    back_button = InlineKeyboardButton(text="<< Назад", callback_data=f"prev_{page_number}")
    next_button = InlineKeyboardButton(text="Вперед >>", callback_data=f"next_{page_number}")
    if page_number == 1 and len(categories) > end_index:
        kb_builder.row(next_button)
    elif page_number > 1 and len(categories) > end_index:
        kb_builder.row(back_button, next_button)
    elif page_number > 1:
        kb_builder.row(back_button)
    if subcategory:
        kb_builder.row(InlineKeyboardButton(text="🔙 В категории", callback_data="category"))
    return kb_builder.as_markup()
