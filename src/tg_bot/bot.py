import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from src.config import config as conf
from src.pkg.logger import log
from src.tg_bot.middleware.repository import DatabaseMiddleware

from .hanlder import router


class TelegramBot:
    def __init__(
        self,
    ) -> None:
        self.bot = Bot(
            token=conf.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        self.dp = Dispatcher(storage=MemoryStorage())
        self.dp.include_router(router)

        self.polling_task = None

    async def start(self) -> None:
        """Запуск бота"""
        self.polling_task = asyncio.create_task(self.dp.start_polling(self.bot))
        log.info("Бот запущен [OK]")

    def setup_middleware(self):
        """Настройка middleware"""
        self.dp.update.middleware(DatabaseMiddleware())

    async def stop(self) -> None:
        """Остановка бота"""
        if self.polling_task:
            self.polling_task.cancel()
            try:
                await self.polling_task
            except asyncio.CancelledError:
                pass
            log.info("Бот остановлен [OK]")

    async def idle(self):
        await self.dp.start_polling(self.bot)
