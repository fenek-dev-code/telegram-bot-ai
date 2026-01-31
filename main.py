import asyncio
from contextlib import asynccontextmanager

from src.pkg.logger import log
from src.tg_bot.bot import TelegramBot


@asynccontextmanager
async def life_span(bot: TelegramBot):
    try:
        await bot.start()
        log.info("Приложение запущено [OK]")
        yield
    finally:
        await bot.stop()
        log.info("Приложение остановлено [OK]")


async def main():
    bot = TelegramBot()
    async with life_span(bot):
        await bot.idle()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Сервер остановлен по запросу пользователя")
    except Exception as e:
        log.critical(f"Критическая ошибка сервера: {e}")
        raise
