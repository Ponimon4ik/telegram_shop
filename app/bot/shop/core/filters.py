from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from aiogram.enums import ChatType, ChatMemberStatus


class IsPrivate(BaseFilter):

    async def __call__(self, update: Message | CallbackQuery) -> bool:
        if isinstance(update, CallbackQuery):
            return update.message.chat.type in ChatType.PRIVATE
        return update.chat.type in ChatType.PRIVATE


class InGroupOrChanel(BaseFilter):

    def __init__(self, chanel_id: str, group_id: str) -> None:
        self.chanel_id = chanel_id
        self.group_id = group_id

    async def __call__(self, message: Message) -> bool:
        bot = message.get_mounted_bot()
        user_id = message.from_user.id
        member_chanel = await bot.get_chat_member(chat_id=self.chanel_id, user_id=user_id)
        member_group = await bot.get_chat_member(chat_id=self.group_id, user_id=user_id)
        return (
            True if member_group and member_chanel not in
               (ChatMemberStatus.KICKED, ChatMemberStatus.LEFT)
            else False
        )
