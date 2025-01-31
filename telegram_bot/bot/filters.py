from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ChatType
from typing import Callable

from main_app.models import User


class StateFilter(Filter):
    def __init__(self, func: Callable[[str], bool]) -> None:
        self.func = func

    async def __call__(self, message: Message, user: User) -> bool:
        return self.func(user.state)

class ChatTypeFilter(Filter):
    async def __call__(self, message: Message | CallbackQuery, user: User) -> bool:
        if isinstance(message, CallbackQuery):
            message = message.message

        return message.chat.type == ChatType.PRIVATE
