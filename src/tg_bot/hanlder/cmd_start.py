from typing import Optional, cast

from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from src.database.repository import Repository
from src.models import User
from src.tg_bot.common import UserKeyboards, UserMessages

router = Router()


@router.message(CommandStart())
@router.callback_query(F.data == UserKeyboards.DATA_HOME_MENU)
async def cmd_start(
    update: types.Message | types.CallbackQuery,
    state: FSMContext,
    repo: Repository,
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
            message=message, user=user, is_callback=True, raw_update=update, repo=repo
        )
    else:
        message = cast(types.Message, update)
        user = cast(types.User, update.from_user)

        await handle_start_request(
            message=message, user=user, is_callback=False, raw_update=update, repo=repo
        )


async def handle_start_request(
    message: types.Message,
    user: types.User,
    is_callback: bool,
    repo: Repository,
    raw_update: types.Message | types.CallbackQuery,
) -> None:
    """Основная логика обработки старта"""
    db_user = await repo.user.get_user(user.id)
    if not db_user:
        referrer_code = ""
        if isinstance(raw_update, types.Message):
            if raw_update.text:
                args = raw_update.text.split()
                referrer_code = args[1] if len(args) > 1 else ""
        db_user = await repo.user.create_user(
            User(id=user.id, ref_code=referrer_code, username=user.username)
        )

    if db_user:
        bot = raw_update.bot if hasattr(raw_update, "bot") else message.bot
        if not bot:
            return
        text = UserMessages.MESSAGE_START
        keyboard = UserKeyboards.home_menu()
        await send_response(
            message=message,
            text=text,
            keyboard=keyboard,
            is_callback=is_callback,
        )


async def send_response(
    message: types.Message,
    text: str,
    keyboard: Optional[types.InlineKeyboardMarkup] = None,
    is_callback: bool = False,
) -> None:
    """Отправка ответа с учетом типа запроса"""

    if is_callback:
        try:
            await message.edit_text(text, reply_markup=keyboard)
        except (AttributeError, TypeError):
            await message.answer(text, reply_markup=keyboard)
    else:
        await message.answer(text, reply_markup=keyboard)
