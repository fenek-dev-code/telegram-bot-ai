from aiogram import types


class CommonFunc:
    @staticmethod
    async def edit_message(
        callback: types.CallbackQuery,
        text: str,
        reply_markup: types.InlineKeyboardMarkup,
    ):
        if callback.bot and callback.message:
            await callback.bot.edit_message_text(
                text=text,
                message_id=callback.message.message_id,
                chat_id=callback.message.chat.id,
                reply_markup=reply_markup,
            )
