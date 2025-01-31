from itertools import batched

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from asgiref.sync import sync_to_async

from .callback_factories import SubmitCallback, GoodsCallback, CategoryCallback, CategoryPageCallback, \
    SubcategoryCallback, SubcategoryPageCallback, BucketCallback
from .texts import *
from config import GROUP_ID, CHANNEL_ID

PER_PAGE = 7


def get_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=CATALOG_BUTTON_TEXT, callback_data='catalog')],
            [InlineKeyboardButton(text=BUCKET_BUTTON_TEXT, callback_data='bucket')],
            [InlineKeyboardButton(text=FAQ_BUTTON_TEXT, switch_inline_query_current_chat='')],
        ]
    )


async def get_category_keyboard(page: int = 0) -> InlineKeyboardMarkup:
    inline_keyboard = list()

    categories = await sync_to_async(Category.objects.all)()
    categories_len = await sync_to_async(len)(categories)
    categories = categories[page * PER_PAGE:(page + 1) * PER_PAGE]

    for pairs in batched(categories, n=2):
        inline_keyboard.append(list())
        for category in pairs:
            inline_keyboard[-1].append(
                InlineKeyboardButton(text=category.name,
                                     callback_data=CategoryCallback(category_id=category.id).pack()))

    inline_keyboard.append(list())
    if page != 0:
        inline_keyboard[-1].append(
            InlineKeyboardButton(text=BACK_BUTTON, callback_data=CategoryPageCallback(page=page - 1).pack())
        )
    if (page + 1) * PER_PAGE < categories_len:
        inline_keyboard[-1].append(
            InlineKeyboardButton(text=FRONT_BUTTON, callback_data=CategoryPageCallback(page=page + 1).pack())
        )

    inline_keyboard.append([InlineKeyboardButton(text=BACK_TO_MENU_BUTTON, callback_data='menu')])

    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


async def get_subcategory_keyboard(category_id: int, page: int = 0) -> InlineKeyboardMarkup:
    inline_keyboard = list()
    subcategories = list()
    async for x in SubcategoryCategory.objects.filter(category__id=category_id):
        subcategory = await sync_to_async(lambda: x.subcategory)()
        subcategories.append(subcategory)

    subcategories_len = await sync_to_async(len)(subcategories)
    subcategories = subcategories[page * PER_PAGE:(page + 1) * PER_PAGE]

    for pairs in batched(subcategories, n=2):
        inline_keyboard.append(list())
        for subcategory in pairs:
            inline_keyboard[-1].append(
                InlineKeyboardButton(
                    text=subcategory.name,
                    callback_data=SubcategoryCallback(subcategory_id=subcategory.id).pack()
                )
            )

    inline_keyboard.append(list())
    if page != 0:
        inline_keyboard[-1].append(
            InlineKeyboardButton(
                text=BACK_BUTTON,
                callback_data=SubcategoryPageCallback(category_id=category_id, page=page - 1).pack())
        )
    if (page + 1) * PER_PAGE < subcategories_len:
        inline_keyboard[-1].append(
            InlineKeyboardButton(
                text=FRONT_BUTTON,
                callback_data=SubcategoryPageCallback(category_id=category_id, page=page + 1).pack()
            )
        )

    inline_keyboard.append([
        InlineKeyboardButton(text=BACK_TO_CATEGORIES_BUTTON, callback_data=CategoryPageCallback(page=0).pack())
    ])

    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def get_goods_keyboard(goods_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BUCKET_GET_OFFER_BUTTON,
                    callback_data=GoodsCallback(goods_id=goods_id).pack()),
            ]
        ]
    )


def get_submit_keyboard(goods_id: int, amount: int = 0) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=CANCEL_BUTTON, callback_data=f'delete'),
                InlineKeyboardButton(
                    text=SUBMIT_BUTTON,
                    callback_data=SubmitCallback(goods_id=goods_id, amount=amount).pack()
                )
            ]
        ]
    )


def get_bucket_keyboard(items_amount) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=DELETE_BUTTON,
                    callback_data=BucketCallback(action='delete', items_amount=items_amount).pack()
                ),
                InlineKeyboardButton(
                    text=GET_ORDER_BUTTON,
                    callback_data=BucketCallback(action='make_order', items_amount=items_amount).pack()
                ),
            ]
            , [InlineKeyboardButton(text=BACK_TO_MENU_BUTTON, callback_data=f'menu')]
        ]
    )


def get_delete_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=CANCEL_BUTTON, callback_data=f'delete')
            ]
        ]
    )


async def get_revizor_keyboard(bot: Bot) -> InlineKeyboardMarkup:
    group_link = (await bot.get_chat(chat_id=GROUP_ID)).invite_link
    channel_link = (await bot.get_chat(chat_id=CHANNEL_ID)).invite_link

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=REVIZOR_GROUP_BUTTON, url=group_link),
                InlineKeyboardButton(text=REVIZOR_CHANNEL_BUTTON, url=channel_link)
            ],
            [
                InlineKeyboardButton(text=REVIZOR_SUBMIT_BUTTON, callback_data='revizor')
            ]
        ]
    )
