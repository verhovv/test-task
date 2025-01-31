from main_app.models import *

# REVIZOR
REVIZOR_SUB_TEXT = '<b>Перед использованием бота</b>, пожалуйста, подпишитесь на канал и войдите в группу'

# buttons
REVIZOR_SUBMIT_BUTTON = '✅ Уже сделано'
REVIZOR_GROUP_BUTTON = '🫂 Группа'
REVIZOR_CHANNEL_BUTTON = '📣 Канал'

CATALOG_BUTTON_TEXT = '🏪 Каталог'
BUCKET_BUTTON_TEXT = '🗑️ Корзина'
FAQ_BUTTON_TEXT = '📰 FAQ'

DELETE_BUTTON = '❌ Удалить товар'
GET_ORDER_BUTTON = '✅ Сделать заказ'

BUCKET_GET_OFFER_BUTTON = '🛒 Заказать'
BACK_TO_MENU_BUTTON = '🔙 Назад в меню 🔙'
BACK_TO_CATEGORIES_BUTTON = '🔙 Назад в категории 🔙'

SUBMIT_BUTTON = '✅ Подтвердить'
CANCEL_BUTTON = '❌ Отменить'

BACK_BUTTON = '⬅️ предыдущая'
FRONT_BUTTON = 'следующая ➡️'

# catalog
CATEGORIES = 'Категории товаров'


def get_subcategory_text(category: Category) -> str:
    return f'{category.name}'


def get_goods_count_text(goods: Goods) -> str:
    return f'❗ Введите количество "{goods.name}", которое вы хотите заказать'


def get_goods_submit_text(goods: Goods, amount: int) -> str:
    return f'Добавить {amount}шт. "{goods.name}" ({goods.cost * amount}руб.) в корзину❔'


def get_goods_added_success_text(goods: Goods, amount: int) -> str:
    return f'✅ Вы успешно добавили {amount}шт. "{goods.name}" в корзину.'


def get_goods_caption(goods: Goods) -> str:
    return f'<b>{goods.name}</b>\n💰 {goods.cost}руб.\n\n{goods.caption}'


# bucket
BUCKET_PLACE = '‼️Введите данные для доставки‼️'
BUCKET_DELETE = '❗Напишите номер товара, который вы хотите удалить из корзины:'
BUCKET_EMPTY = 'Ваша корзина пуста 🗑️'
BUCKET_TOP = '🗑️ Ваша корзина:\n\n'


def get_bucket_delete_success_text(goods_name: str) -> str:
    return f'✅ Вы успешно удалили "{goods_name}" из корзины'


def get_bucket_item_text(number: int, name: str, amount: int, cost: int) -> str:
    return f'{number}. <b>"{name}" {amount}шт.</b> | {cost}руб\n'


def get_bucket_bottom_text(at_all: int) -> str:
    return f'\nВсего: {at_all}'


def get_bucket_link_text(link: str) -> str:
    return f'<i>Пройдите по следующей ссылке для завершения оплаты:</i>\n\n{link}'


# payment
def get_payment_succeed_text(user: User, place: str) -> str:
    return f'✅ <b>Вы успешно оплатили товар</b>\n\n' + \
        f'В скором времени он прибудет на место доставки:\n{place}'


def get_payment_canceled_text(user: User) -> str:
    return f'❌ <b>Оплата не прошла</b>.\nМожете попробовать в другое время.'


def get_menu_text(user: User) -> str:
    return f"<b>Доброго времени суток, {user.first_name}!</b>"


# errors
INVALID_VALUE = '<b>Что-то пошло не так</b>.\nВведите валидное значение.'
