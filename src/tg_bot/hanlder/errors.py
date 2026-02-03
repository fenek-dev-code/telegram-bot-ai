from aiogram import Router
from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramNetworkError,
    TelegramNotFound,
)
from aiogram.types import ErrorEvent

from src.pkg.logger import log

router = Router()


@router.error()
async def error_handler(event: ErrorEvent):
    exception = event.exception

    # 1. Ошибка "message is not modified" - игнорируем
    if isinstance(exception, TelegramBadRequest):
        error_message = str(exception).lower()

        if "message is not modified" in error_message:
            return True

        if "message to edit not found" in error_message:
            log.error(f"Сообщение не найдено для редактирования")
            return True

        if "message can't be deleted" in error_message:
            # Нельзя удалить сообщение
            log.error(f"Не могу удалить сообщение")
            return True

    # 2. Сообщение не найдено (уже удалено)
    elif isinstance(exception, TelegramNotFound):
        if "message to delete not found" in str(exception):
            log.error("Сообщение для удаления не найдено")
            return True

    # 3. Бота заблокировали
    elif isinstance(exception, TelegramForbiddenError):
        log.error(f"Пользователь заблокировал бота: {event.update}")
        return True

    # 4. Проблемы с сетью
    elif isinstance(exception, TelegramNetworkError):
        log.error(f"Проблема с сетью: {exception}")
        return True
