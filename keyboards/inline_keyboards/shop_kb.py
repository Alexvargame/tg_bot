from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from random import randint


class ShopActions(IntEnum):
    products = auto()
    address = auto()
    root = auto()

class ProductActions(IntEnum):
    detail = auto()
    update = auto()
    delete = auto()
class ShopCbData(CallbackData, prefix='shop'):
    action: ShopActions

class ProductCbData(CallbackData, prefix='product'):
    action: ProductActions
    id: int
    title: str
    price: int
def build_shop_kb():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Show products',
        callback_data=ShopCbData(action=ShopActions.products).pack(),
    )
    builder.button(
        text='My address',
        callback_data=ShopCbData(action=ShopActions.address).pack(),
    )

    builder.adjust(1)
    return builder.as_markup()



def build_products_kb():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Back to root',
        callback_data=ShopCbData(action=ShopActions.root).pack(),
    )
    for idx, (name, price) in enumerate([
        ('Tablet', 999),
        ('Laptop', 1299),
        ('Desktop', 2499)
    ], start=1):
        builder.button(
            text=name,
            callback_data=ProductCbData(
                action=ProductActions.detail,
                id=idx,
                title=name,
                price=price)
        )
    builder.adjust(1)
    return builder.as_markup()


def build_product_detail_kb(product_cb_data: ProductCbData):
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Back to products',
        callback_data=ShopCbData(action=ShopActions.products).pack(),
    )
    for label, action in [('update', ProductActions.update), ('delete', ProductActions.delete)]:
        builder.button(
            text=label,
            callback_data=ProductCbData(
                action=action,
                **product_cb_data.model_dump(include={'id', 'title', 'price'}),
            )
        )

    builder.adjust(1, 2)
    return builder.as_markup()

def build_update_product_kb(product_cb_data: ProductCbData):
    print('update')
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f'Back to product {product_cb_data.title}',
        callback_data=ProductCbData(
            action=ProductActions.detail,
            **product_cb_data.model_dump(include={'id', 'title', 'price'}),
        ),
    )
    builder.button(
        text='Update',
        callback_data='...'
    )
    builder.adjust(1)
    return builder.as_markup()