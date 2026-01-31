from aiogram import F, Router, types

from src.core.service import UserService
from src.database import get_session
from src.tg_bot.buttons import CallBackData, UserButtons
from src.tg_bot.common import ReplyMessages, edit_message

router = Router()


@router.callback_query(F.data == CallBackData.GENERATE_VIDEO)
async def generate_video(callback_query: types.CallbackQuery):
    await edit_message(
        callback_query,
        text=ReplyMessages.generate_video(),
        reply_markup=UserButtons.go_home(),
    )


@router.callback_query(F.data == CallBackData.GENERATE_IMAGE)
async def generate_image(callback_query: types.CallbackQuery):
    await edit_message(
        callback_query,
        text=ReplyMessages.generate_image(),
        reply_markup=UserButtons.go_home(),
    )
