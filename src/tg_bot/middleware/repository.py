# middlewares/minimal_db.py
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.database import get_session
from src.database.repository import Repository
from src.pkg.logger import log


class DatabaseMiddleware(BaseMiddleware):
    """Middleware для работы с базой данных"""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with get_session() as session:
            data["repo"] = Repository(session)
            try:
                result = await handler(event, data)
                if session.dirty or session.new or session.deleted:
                    await session.commit()
                return result

            except Exception as error:
                log.error(f"Error: {error}", exc_info=True)
                if session.is_active:
                    await session.rollback()
                raise
