import math

from core.keyboards.category_keyboard import create_catalog_keyboard, ITEMS_PER_PAGE

CATALOG_PAGE = 'Категории: страница {current_page}/{pages_quantity}'
SUBCATEGORIES_PAGE = '{title}: страница {current_page}/{pages_quantity}'
PRODUCT_NO_EXIST = 'Упс, кажется здесь ничего нет'


def create_catalog_message(categories: list, is_subcategory=False, current_page: int = 1) -> dict:
    categories_quantity = len(categories)
    pages_quantity = math.ceil(categories_quantity / ITEMS_PER_PAGE)
    if len(categories) == 0:
        text = PRODUCT_NO_EXIST
    elif is_subcategory:
        text = SUBCATEGORIES_PAGE.format(
            title=categories[0]['title'], current_page=current_page, pages_quantity=pages_quantity
        )
    else:
        text = CATALOG_PAGE.format(current_page=current_page, pages_quantity=pages_quantity)
    return {
        'text': text,
        'reply_markup': create_catalog_keyboard(
            page_number=current_page, categories=categories, subcategory=is_subcategory
        )
    }
