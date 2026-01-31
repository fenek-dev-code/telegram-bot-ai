from logging import log
from typing import Optional, cast

from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from src.core.service import UserService
from src.database import get_session
from src.pkg.logger import log
from src.tg_bot.buttons import UserButtons
from src.tg_bot.common.reply_messages import ReplyMessages

router = Router()


@router.message(CommandStart())
@router.callback_query(F.data == "start")
async def cmd_start(
    update: types.Message | types.CallbackQuery, state: FSMContext
) -> None:
    """Версия с кастингом типов"""
    await state.clear()
    # Приводим типы явно
    if isinstance(update, types.CallbackQuery):
        callback = cast(types.CallbackQuery, update)
        message = cast(types.Message, callback.message)
        user = cast(types.User, callback.from_user)

        await callback.answer()

        # Обрабатываем callback
        await handle_start_request(
            message=message, user=user, is_callback=True, raw_update=update
        )
    else:
        message = cast(types.Message, update)
        user = cast(types.User, update.from_user)

        await handle_start_request(
            message=message, user=user, is_callback=False, raw_update=update
        )


async def handle_start_request(
    message: types.Message,
    user: types.User,
    is_callback: bool,
    raw_update: types.Message | types.CallbackQuery,
) -> None:
    """Основная логика обработки старта"""

    async with get_session() as session:
        try:
            service = UserService(session)

            # Получаем пользователя
            db_user = await service.get_user(user.id)

            # Если нет - создаем
            if not db_user:
                referrer_code = ""

                # Извлекаем код только из текстовой команды
                if isinstance(raw_update, types.Message):
                    if raw_update.text:
                        args = raw_update.text.split()
                        referrer_code = args[1] if len(args) > 1 else ""

                db_user = await service.create_user(
                    id=user.id, ref_code=referrer_code, username=user.username
                )

            if db_user:
                bot = raw_update.bot if hasattr(raw_update, "bot") else message.bot
                if not bot:
                    return

                text = ReplyMessages.start_message(db_user)
                keyboard = UserButtons.get_home_menu()

                # Отправляем
                await send_response(
                    message=message,
                    text=text,
                    keyboard=keyboard,
                    is_callback=is_callback,
                )
        except Exception as err:
            log.error(err)
            return


async def send_response(
    message: types.Message,
    text: str,
    keyboard: Optional[types.InlineKeyboardMarkup] = None,
    is_callback: bool = False,
) -> None:
    """Отправка ответа с учетом типа запроса"""

    if is_callback:
        # Для callback
        try:
            await message.edit_text(text, reply_markup=keyboard)
        except (AttributeError, TypeError):
            # Если нельзя редактировать
            await message.answer(text, reply_markup=keyboard)
    else:
        # Для команды
        await message.answer(text, reply_markup=keyboard)
