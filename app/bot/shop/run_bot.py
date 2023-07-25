import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.types import BotCommand

from core.handlers import routers


from settings.config import config


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start', description='Начало работы'),
    ]

    await bot.set_my_commands(main_menu_commands)


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    redis: Redis = Redis(
        host=config.redis.rd_host,
        password=config.redis.rd_password,
        port=config.redis.rd_port
    )
    bot: Bot = Bot(token=config.tg_bot.token)
    storage: RedisStorage = RedisStorage(redis=redis)
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.include_routers(*routers)
    dp.startup.register(set_main_menu)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
