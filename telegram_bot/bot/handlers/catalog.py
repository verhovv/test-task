from aiogram import Router, F
from aiogram.types import FSInputFile

from ..filters import *
from ..keyboards import *
from ..callback_factories import *
from ..texts import *

from main_app.models import *

from asgiref.sync import sync_to_async
from .bucket import do_bucket_message

router = Router()


@router.callback_query(F.data == 'catalog')
async def on_catalog_callback(callback: CallbackQuery):
    await callback.message.edit_text(text=CATEGORIES, reply_markup=await get_category_keyboard())


@router.callback_query(CategoryPageCallback.filter())
async def on_category_page_callback(callback: CallbackQuery, callback_data: CategoryPageCallback):
    await callback.message.edit_text(
        text=CATEGORIES,
        reply_markup=await get_category_keyboard(page=callback_data.page)
    )


@router.callback_query(CategoryCallback.filter())
async def on_category_callback(callback: CallbackQuery, callback_data: CategoryCallback):
    await callback.message.edit_text(
        text=get_subcategory_text(category=await Category.objects.aget(id=callback_data.category_id)),
        reply_markup=await get_subcategory_keyboard(category_id=callback_data.category_id)
    )


@router.callback_query(SubcategoryPageCallback.filter())
async def on_subcategory_page_callback(callback: CallbackQuery, callback_data: SubcategoryPageCallback):
    await callback.message.edit_reply_markup(
        reply_markup=await get_subcategory_keyboard(callback_data.category_id, callback_data.page)
    )


@router.callback_query(SubcategoryCallback.filter())
async def on_category_callback(callback: CallbackQuery, callback_data: SubcategoryCallback):
    async for x in SubcategoryGoods.objects.filter(subcategory__id=callback_data.subcategory_id):
        goods = await sync_to_async(lambda: x.goods)()
        await callback.message.answer_photo(
            photo=FSInputFile(path=f'../{goods.image.name}'),
            caption=get_goods_caption(goods=goods),
            reply_markup=get_goods_keyboard(goods.id)
        )

    subcategory_category = await SubcategoryCategory.objects.aget(subcategory__id=callback_data.subcategory_id)
    category = await sync_to_async(lambda: subcategory_category.category)()

    await callback.message.answer(
        text=get_subcategory_text(category=category),
        reply_markup=await get_subcategory_keyboard(category.id, 0)
    )


@router.callback_query(GoodsCallback.filter())
async def on_goods_callback(callback: CallbackQuery, callback_data: GoodsCallback, user: User):
    goods = await Goods.objects.aget(id=callback_data.goods_id)

    message = await callback.message.answer(text=get_goods_count_text(goods=goods), reply_markup=get_delete_keyboard())

    user.state = f'goods_{callback_data.goods_id}_{message.message_id}'
    await user.asave()


@router.message(StateFilter(lambda state: state.startswith('goods')))
async def on_goods_state_message(message: Message, user: User, bot: Bot):
    try:
        amount = int(message.text)

        if amount <= 0:
            raise ValueError

    except ValueError:
        await message.answer(text=INVALID_VALUE)
        return

    message_id = int(user.state.split('_')[2])

    goods_id = int(user.state.split('_')[1])
    goods = await Goods.objects.aget(id=goods_id)

    user.state = 'start'
    await user.asave()

    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.delete()

    await message.answer(
        text=get_goods_submit_text(goods=goods, amount=amount),
        reply_markup=get_submit_keyboard(goods.id, amount)
    )


@router.callback_query(SubmitCallback.filter())
async def on_submit_callback(callback: CallbackQuery, callback_data: SubmitCallback, user: User):
    goods = await Goods.objects.aget(id=callback_data.goods_id)
    amount = callback_data.amount

    await UserBucket.objects.acreate(user=user, goods=goods, amount=amount)

    await callback.message.delete()
    await callback.message.answer(text=get_goods_added_success_text(goods=goods, amount=amount))
    await do_bucket_message(message=callback.message, user=user)


@router.callback_query(F.data == 'delete')
async def on_delete_callback(callback: CallbackQuery, user: User):
    await callback.message.delete()
    user.state = 'start'
    await user.asave()
