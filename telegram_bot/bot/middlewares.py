from typing import Callable, Any, Dict, Awaitable
from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ChatMemberStatus, ChatType

from main_app.models import User
from .keyboards import get_revizor_keyboard
from .texts import REVIZOR_SUB_TEXT
from config import CHANNEL_ID, GROUP_ID


class UserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        from_user = event.from_user

        try:
            user = await User.objects.aget(id=from_user.id)
        except User.DoesNotExist:
            user = await User.objects.acreate(
                id=from_user.id,
                username=from_user.username or 'hidden',
                first_name=from_user.first_name or '',
                last_name=from_user.last_name or '',
                state='start'
            )

        data['user'] = user

        return await handler(event, data)


class RevizorMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id

        bot: Bot = data['bot']

        group_member = await bot.get_chat_member(chat_id=GROUP_ID, user_id=user_id)
        channel_member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)

        if ChatMemberStatus.LEFT in [group_member.status, channel_member.status]:
            if isinstance(event, CallbackQuery):
                message: Message = event.message
                await event.answer()
            if isinstance(event, Message):
                message: Message = event

            await message.answer(text=REVIZOR_SUB_TEXT, reply_markup=await get_revizor_keyboard(bot))
            return

        return await handler(event, data)
