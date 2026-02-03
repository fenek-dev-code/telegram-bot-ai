from aiogram import F, Router, types

from src.database.repository import Repository
from src.models import PaymentType
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


# Кнопка генерация видео:
@router.callback_query(F.data == UserKeyboards.DATA_GENERATE_VIDEO)
async def video_menu(callback: types.CallbackQuery):
    return await CommonFunc.edit_message(
        callback,
        UserMessages.MESSAGE_GENERATE_VIDEO,
        UserKeyboards.user_info_menu(UserKeyboards.DATA_HOME_MENU),
    )


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
                referal_code=user.referal_code,
                referal_count=len(referals),
                transactions=transactions,
            ),
            UserKeyboards.referals_button(referals),
        )


# TODO:
@router.callback_query(F.data.startswith(CallBackData.REFERAL_USER_PREFIX))
async def referal_info(callback: types.CallbackQuery):
    if callback.data:
        try:
            user_id = int(callback.data.split(":")[1])
        except Exception:
            return callback.answer("Ошибка при получении Реферала")
        referal = await service.get_user_stat(user_id)
        if callback.message and callback.bot:
            await callback.answer()
            return await edit_message(
                callback=callback,
                text=ReplyMessages.referal_info(referal),
                reply_markup=UserButtons.go_home(),
            )
