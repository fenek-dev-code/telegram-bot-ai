from aiogram import F, Router, types

from src.core.service import UserService
from src.database import get_session
from src.tg_bot.buttons import CallBackData, UserButtons
from src.tg_bot.common import ReplyMessages, edit_message

router = Router()


@router.callback_query(F.data == CallBackData.REFERAL_SYSTEM)
async def referal_system_button(call_back: types.CallbackQuery):
    async with get_session() as session:
        service = UserService(session)
        referals = await service.get_referal_users(call_back.from_user.id)
        user = await service.get_user(call_back.from_user.id)
        bot_name: str = ""

        if call_back.bot and user and call_back.message:
            bot = (await call_back.bot.get_me()).username
            if bot:
                bot_name += bot

            call_back.answer("Loading...")
            if len(referals) > 0:
                return await edit_message(
                    callback=call_back,
                    text=ReplyMessages.referals_message(
                        user_name=call_back.from_user.full_name,
                        have_referals=True,
                        ref_link=user.generate_referral_link(bot_name),
                    ),
                    reply_markup=UserButtons.referals_button(referals),
                )
            return await edit_message(
                callback=call_back,
                text=ReplyMessages.referals_message(
                    user_name=call_back.from_user.full_name,
                    have_referals=True,
                    ref_link=user.generate_referral_link(bot_name),
                ),
                reply_markup=UserButtons.referals_button(referals),
            )


@router.callback_query(F.data.startswith(CallBackData.REFERAL_USER_PREFIX))
async def referal_info(callback: types.CallbackQuery):
    async with get_session() as session:
        service = UserService(session)
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
