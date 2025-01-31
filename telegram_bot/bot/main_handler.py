from aiogram import Router, filters, F
from aiogram.types import Message, CallbackQuery

from main_app.models import User
from .keyboards import get_menu_keyboard
from .handlers import *
from .texts import *

router = Router()

router.include_routers(
    revizor.router,
    faq.router,
    catalog.router,
    bucket.router
)

@router.message(filters.CommandStart())
async def on_start_command(message: Message, user: User):
    await message.answer(text=get_menu_text(user=user), reply_markup=get_menu_keyboard())

@router.callback_query(F.data == 'menu')
async def on_menu_callback(callback: CallbackQuery, user: User):
    await callback.message.edit_text(text=get_menu_text(user=user), reply_markup=get_menu_keyboard())