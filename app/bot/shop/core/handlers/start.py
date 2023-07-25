from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, Update, CallbackQuery

from core.keyboards import menu_keyboard
from core.db.user import get_or_create_tguser
from core.filters import IsPrivate, InGroupOrChanel
from settings.config import config

router = Router()
router.message.filter(IsPrivate())

NO_SUBSCRIBE = 'Что бы продолжить работу с ботом подпишитесь на группу {0} и канал {1}'


@router.callback_query(
    ~InGroupOrChanel(chanel_id=config.tg_bot.canal_id, group_id=config.tg_bot.canal_id)
)
@router.message(
    ~InGroupOrChanel(chanel_id=config.tg_bot.canal_id, group_id=config.tg_bot.group_id)
)
async def no_subscribe(update: Update):
    message = update
    if isinstance(message, CallbackQuery):
        message = update.message
    await message.answer(text=NO_SUBSCRIBE.format(config.tg_bot.canal_id, config.tg_bot.canal_id))


@router.message(CommandStart())
async def cmd_start(message: Message):
    await get_or_create_tguser(tg_id=message.from_user.id)
    await message.answer(text='Hello', reply_markup=menu_keyboard.keyboard)
