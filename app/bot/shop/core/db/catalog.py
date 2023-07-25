from core.db.db import connection, to_dict


@connection
async def get_all_categories(db):
    cursor = await db.execute("SELECT * FROM goods_category ")
    categories = await to_dict(cursor)
    return categories


@connection
async def get_subcategories_for_category(db, category_id):
    cursor = await db.execute(
        "SELECT * FROM goods_subcategory WHERE category_id=? ", (category_id, )
    )
    subcategories = await to_dict(cursor)
    return subcategories
