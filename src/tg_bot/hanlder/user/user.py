from aiogram import F, Router, types

from src.database.models import PaymentType
from src.database.repository import Repository
from src.tg_bot.common import CommonFunc, UserKeyboards, UserMessages

router = Router()


# Личный кабинет
@router.callback_query(F.data == UserKeyboards.DATA_USER_INFO_MENU)
async def user_info_menu(callback: types.CallbackQuery):
    return await CommonFunc.edit_message(
        callback,
        UserMessages.MESSAGE_USER_INFO_MENU,
        UserKeyboards.user_info_menu(UserKeyboards.DATA_HOME_MENU),
    )


# Профиль Пользователя
@router.callback_query(F.data == UserKeyboards.DATA_USER_INFO)
async def user_info_button(call_back: types.CallbackQuery, repo: Repository):
    user = await repo.user.get_user_with_deps(call_back.from_user.id)
    if user:
        await call_back.answer("Loading...")
        return await CommonFunc.edit_message(
            call_back,
            UserMessages.message_user_info(user),
            UserKeyboards.back_to(UserKeyboards.DATA_USER_INFO_MENU),
        )
    else:
        await call_back.answer("User not found")


# REFERAL SYSTEM
# Список рефералов и инфомация
@router.callback_query(F.data == UserKeyboards.DATA_USER_REFERRAL)
async def referal_system_button(call_back: types.CallbackQuery, repo: Repository):
    referals = await repo.user.get_users_by_refer_id(call_back.from_user.id)
    user = await repo.user.get_user(call_back.from_user.id)
    transactions = await repo.transaction.get_transactions_by_user_id(
        call_back.from_user.id, payment_type=PaymentType.REFERRAL
    )
    bot_name: str = ""
    if call_back.bot and user and call_back.message:
        bot_name += str((await call_back.bot.get_me()).username)

        await call_back.answer("Loading...")
        return await CommonFunc.edit_message(
            call_back,
            UserMessages.referals_message(
                botname=bot_name,
                referal_code=user.referral_code,
                referal_count=len(referals),
                transactions=transactions,
            ),
            UserKeyboards.referals_button(referals, UserKeyboards.DATA_USER_INFO_MENU),
        )


# Информация о реферале
@router.callback_query(F.data.startswith(UserKeyboards.DATA_USER_REFERRAL))
async def referal_info(callback: types.CallbackQuery, repo: Repository):
    if callback.data:
        try:
            user_id = int(callback.data.split(":")[1])
        except Exception:
            return callback.answer("Ошибка при получении Реферала")
        referal = await repo.user.get_user_with_deps(user_id)
        if callback.message and callback.bot:
            await callback.answer()
            return await CommonFunc.edit_message(
                callback=callback,
                text=UserMessages.message_referal_info(referal),
                reply_markup=UserKeyboards.back_to(UserKeyboards.DATA_USER_INFO_MENU),
            )
