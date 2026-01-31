from aiogram import Router
from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramNetworkError,
    TelegramNotFound,
)
from aiogram.types import ErrorEvent

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
            # Сообщение было удалено
            print(f"Сообщение не найдено для редактирования")
            return True

        if "message can't be deleted" in error_message:
            # Нельзя удалить сообщение
            print(f"Не могу удалить сообщение")
            return True

    # 2. Сообщение не найдено (уже удалено)
    elif isinstance(exception, TelegramNotFound):
        if "message to delete not found" in str(exception):
            print("Сообщение для удаления не найдено")
            return True

    # 3. Бота заблокировали
    elif isinstance(exception, TelegramForbiddenError):
        print(f"Пользователь заблокировал бота: {event.update}")
        return True

    # 4. Проблемы с сетью
    elif isinstance(exception, TelegramNetworkError):
        print(f"Проблема с сетью: {exception}")
        # Можно попробовать повторить запрос
        return True

    # 5. Все остальные ошибки - логируем
    print(f"Необработанная ошибка: {type(exception).__name__}: {exception}")
    print(f"Update: {event.update}")

    return True  # Ошибка обработана
