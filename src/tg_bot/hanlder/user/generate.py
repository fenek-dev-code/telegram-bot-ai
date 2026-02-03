from aiogram import Bot, F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.database.repository import Repository
from src.tg_bot.common import CommonFunc, UserKeyboards, UserMessages

router = Router()


class GenerateVideoStates(StatesGroup):
    waiting_prompt = State()
    waiting_generate = State()


# Кнопка генерация видео:
@router.callback_query(F.data == UserKeyboards.DATA_GENERATE_VIDEO)
async def video_menu(callback: types.CallbackQuery, state: FSMContext):
    return await CommonFunc.edit_message(
        callback,
        UserMessages.MESSAGE_GENERATE_VIDEO,
        UserKeyboards.select_models(UserKeyboards.DATA_USER_INFO_MENU),
    )


@router.message(StateFilter(GenerateVideoStates.waiting_prompt) and F.photo)
async def prompt_message(message: types.Message, state: FSMContext, bot: Bot):
    text = message.caption
    if message.photo:
        if len(message.photo) > 1:
            await message.answer("Пожалуйста отправьте одно фото")
            return
        file = message.photo[0].file_id
        await bot.download_file(file)
