from aiogram import Router
from .info_keyboard_callback_handler import router as info_keyboard_callback_router
from .actions_keyboard_callback_handler import router as actions_keyboard_callback_router
from .shop_keyboard_callback_handler import router as shop_keyboard_callback_router

router = Router(name=__name__)

router.include_routers(
    info_keyboard_callback_router,
    actions_keyboard_callback_router,
    shop_keyboard_callback_router
)

