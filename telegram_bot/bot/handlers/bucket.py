from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from main_app.models import *
from ..filters import *
from ..keyboards import *
from ..callback_factories import *

from . import payment
from ..texts import BUCKET_TOP, get_bucket_item_text, get_bucket_bottom_text, BUCKET_EMPTY, BUCKET_PLACE, \
    get_bucket_delete_success_text, INVALID_VALUE, get_bucket_link_text

router = Router()


async def do_bucket_message(message: Message, user: User, edit=False) -> None:
    text = BUCKET_TOP

    at_all = 0

    user_bucket = await sync_to_async(UserBucket.objects.filter)(user=user)
    user_bucket_len = await sync_to_async(len)(user_bucket)

    for i, bucket in enumerate(user_bucket, 1):
        goods = await sync_to_async(lambda: bucket.goods)()

        cost = goods.cost * bucket.amount
        text += get_bucket_item_text(number=i, name=goods.name, amount=bucket.amount, cost=cost)

        at_all += cost

    text += get_bucket_bottom_text(at_all=at_all)

    if not at_all:
        await message.answer(text=get_menu_text(user=user), reply_markup=get_menu_keyboard())
        return

    if edit:
        await message.edit_text(text=text, reply_markup=get_bucket_keyboard(user_bucket_len))
    else:
        await message.answer(text=text, reply_markup=get_bucket_keyboard(user_bucket_len))


@router.callback_query(F.data == 'bucket')
async def on_bucket_callback(callback: CallbackQuery, user: User):
    user_bucket = await sync_to_async(UserBucket.objects.filter)(user=user)
    if not await sync_to_async(lambda: bool(user_bucket))():
        await callback.answer(text=BUCKET_EMPTY, show_alert=True)
        return

    await do_bucket_message(message=callback.message, user=user, edit=True)


@router.callback_query(BucketCallback.filter())
async def on_bucket_callback(callback: CallbackQuery, callback_data: BucketCallback, user: User):
    if callback_data.action == 'make_order':
        await callback.message.answer(text=BUCKET_PLACE)
        user.state = 'making_order'
        await user.asave()
        return

    message = await callback.message.answer(text=BUCKET_DELETE, reply_markup=get_delete_keyboard())
    user.state = f'deleting_item_{callback_data.items_amount}_{message.message_id}'
    await user.asave()


@router.message(StateFilter(lambda state: state.startswith('deleting_item_')))
async def on_deleting_item_message(message: Message, user: User, bot: Bot):
    item_amount = int(user.state.split('_')[2])
    message_id = int(user.state.split('_')[3])

    try:
        number = int(message.text)

        if number < 1 or number > item_amount:
            raise ValueError
    except ValueError:
        await message.answer(text=INVALID_VALUE)
        return

    user_bucket = await sync_to_async(UserBucket.objects.filter)(user=user)
    user_bucket_item = await sync_to_async(lambda: user_bucket[number - 1])()

    goods = await sync_to_async(lambda: user_bucket_item.goods)()

    await user_bucket_item.adelete()
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.answer(text=get_bucket_delete_success_text(goods.name))
    await do_bucket_message(message=message, user=user)

    user.state = 'start'
    await user.asave()


@router.message(StateFilter(lambda x: x == 'making_order'))
async def on_making_order(message: Message, user: User, bot: Bot):
    await message.answer(
        text=get_bucket_link_text(
            link=await payment.get_link(
                user=user,
                place=message.text,
                bot=bot
            )
        )
    )

    user.state = 'start'
    await user.asave()
