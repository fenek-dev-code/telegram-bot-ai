from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ErrorEvent

from .balance import router as balance_router
from .cmd_start import router as start_router
from .generate import router as generate_router
from .user import router as user_router

router = Router()


@router.error()
async def error_handler(event: ErrorEvent):
    """
    event.exception - само исключение
    event.update - апдейт, который вызвал ошибку
    """
    if isinstance(event.exception, TelegramBadRequest):
        if "message is not modified" in str(event.exception):
            return True

    print(f"Необработанное исключение: {event.exception}")

    return True


router.include_routers(user_router, start_router, generate_router, balance_router)


__all__ = ["router"]
