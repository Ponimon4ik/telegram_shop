from functools import wraps

import aiosqlite
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

DB_FILE = BASE_DIR / 'db' / 'db.sqlite3'


async def to_dict(cursor):
    columns = [column[0] for column in cursor.description]
    rows = await cursor.fetchall()
    return [dict(zip(columns, row)) for row in rows]


async def create_connection():
    return await aiosqlite.connect(DB_FILE)


async def close_connection(db):
    await db.close()


def connection(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        db = await create_connection()
        try:
            result = await func(db, *args, **kwargs)
            await db.commit()
            return result
        finally:
            await close_connection(db)
    return wrapper
