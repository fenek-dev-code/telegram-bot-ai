from aiogram import Router

from .balance import router as balance_router
from .cmd_start import router as start_router
from .generate import router as generate_router
from .user import router as user_router

router = Router()
router.include_routers(user_router, start_router, generate_router, balance_router)

__all__ = ["router"]
