from random import randint

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from keyboards.inline_keyboards.shop_kb import (
    ShopCbData,
    ShopActions,
    build_shop_kb,
    build_products_kb,
    ProductActions,
    ProductCbData,
    build_product_detail_kb,
    build_update_product_kb,
)

router = Router(name=__name__)

@router.callback_query(ShopCbData.filter(F.action == ShopActions.products))
async def send_products_list(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        text=f"Avaliable products",
        reply_markup=build_products_kb(),
    )

@router.callback_query(ShopCbData.filter(F.action == ShopActions.address))
async def handle_my_address_button(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.answer(
        text=f"Your address section is still in progress...",
        cache_time=30,
    )


@router.callback_query(ShopCbData.filter(F.action == ShopActions.root))
async def handle_my_address_button(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Your shop actions:",
        reply_markup=build_shop_kb(),
    )

@router.callback_query(ProductCbData.filter(F.action == ProductActions.detail))
async def handle_product_detail_button(callback_query: CallbackQuery, callback_data: ProductCbData):
    message_text = markdown.text(
        markdown.hbold(f'Product №{callback_data.id}'),
        markdown.text(
            markdown.hbold("Title:"),
            callback_data.title
        ),
        markdown.text(
            markdown.hbold("Price:"),
            callback_data.price
        ),
        sep='\n'
    )
    await callback_query.answer()
    await callback_query.message.edit_text(
        text=message_text,
        reply_markup=build_product_detail_kb(callback_data),
    )

@router.callback_query(ProductCbData.filter(F.action == ProductActions.update))
async def handle_product_update_button(callback_query: CallbackQuery, callback_data:ProductCbData):

    await callback_query.answer()
    await callback_query.message.edit_reply_markup(
        reply_markup=build_update_product_kb(callback_data)
    )

@router.callback_query(ProductCbData.filter(F.action == ProductActions.delete))
async def handle_product_delete_button(callback_query: CallbackQuery):

    await callback_query.answer(
        text='Delete is still in progress...'
    )
