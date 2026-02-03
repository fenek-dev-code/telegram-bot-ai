from aiogram import Router

from .cmd_start import router as start_router
from .errors import router as error_router
from .user.balance import router as balance_router
from .user.user import router as user_router

router = Router()

router.include_routers(error_router, user_router, start_router, balance_router)


__all__ = ["router"]
