from core.db.db import connection, to_dict


@connection
async def get_tguser(db, tg_id):
    cursor = await db.execute(
        "SELECT id FROM tg_users_tguser WHERE tg_id = ?", (tg_id,)
    )
    user = await to_dict(cursor)
    return user


@connection
async def create_tguser(db, tg_id):
    cursor = await db.execute(
        "INSERT INTO tg_users_tguser (tg_id) VALUES (?)", (tg_id,)
    )
    user_id = cursor.lastrowid
    return user_id


@connection
async def get_or_create_tguser(db, tg_id):
    user = await get_tguser(tg_id=tg_id)
    if not user:
        await create_tguser(tg_id=tg_id)
    user = await get_tguser(tg_id=tg_id)
    return user
