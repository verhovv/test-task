from aiogram.filters.callback_data import CallbackData


class SubmitCallback(CallbackData, prefix='submit'):
    goods_id: int
    amount: int


class GoodsCallback(CallbackData, prefix='goods'):
    goods_id: int


class CategoryCallback(CallbackData, prefix='category'):
    category_id: int


class CategoryPageCallback(CallbackData, prefix='category_page'):
    page: int


class SubcategoryCallback(CallbackData, prefix='subcategory'):
    subcategory_id: int


class SubcategoryPageCallback(CallbackData, prefix='subcategory_page'):
    category_id: int
    page: int


class BucketCallback(CallbackData, prefix='bucket'):
    action: str
    items_amount: int
