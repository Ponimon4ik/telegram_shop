from core.db.db import connection, to_dict


@connection
async def get_product(db, products_id: int):
    cursor = await db.execute(
        "SELECT * FROM goods_product WHERE id=?", (products_id,)
    )
    product = await to_dict(cursor)
    if len(product) == 0:
        return None
    return product[0]


@connection
async def get_products_for_subcategory(db, subcategory_id: int, cart_products_ids: list):
    if cart_products_ids:
        cart_products_ids = ','.join(str(products_id) for products_id in cart_products_ids)
        additional_condition = f'(products.quantity > 0 OR products.id IN ({cart_products_ids}))'
    else:
        additional_condition = 'products.quantity > 0'
    query = (
        f"SELECT products.*, subcategory.title AS subcategory_title "
        f"FROM goods_product AS products "
        f"JOIN goods_subcategory AS subcategory ON products.subcategory_id = subcategory.id "
        f"WHERE products.subcategory_id={subcategory_id} AND {additional_condition}"
    )
    cursor = await db.execute(query)
    products = await to_dict(cursor)
    return products


@connection
async def get_products_for_cart(db, product_ids: tuple):
    if not product_ids:
        return []
    product_ids = ','.join(str(products_id) for products_id in product_ids)
    cursor = await db.execute(
        f"SELECT * FROM goods_product WHERE id IN ({product_ids})"
    )
    products = await to_dict(cursor)
    return products
