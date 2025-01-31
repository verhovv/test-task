from aiogram import Router, F
from aiogram.types import CallbackQuery

from main_app.models import User
from ..keyboards import get_menu_keyboard
from ..texts import get_menu_text

router = Router()


@router.callback_query(F.data == 'revizor')
async def on_revizor_callback(callback: CallbackQuery, user: User):
    await callback.message.answer(text=get_menu_text(user=user), reply_markup=get_menu_keyboard())
