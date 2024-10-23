__all__ = ('router',)
from aiogram import Router

from .commands import router as commands_router
from .common import router as common_router
from .media_handlers import router as media_handlers_router
from .admin_handlers import router as admin_handlers_router
from .callback_handlers import router as callback_router
from .survey import router as survey_router

router = Router(name=__name__)

router.include_routers(
    callback_router,
    commands_router,
    survey_router,
    media_handlers_router,
    admin_handlers_router,

)

#last registry
router.include_router(common_router)