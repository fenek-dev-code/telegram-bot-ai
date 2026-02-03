from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


class PaymentKeyboard:
    DATA_CHECK: str = "PAYMENT_CHECK"
    DATA_CANCEL: str = "PAYMENT_CANCEL"

    @staticmethod
    def get_payment_keyboard(url: str) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            InlineKeyboardButton(
                text="Проверить", callback_data=PaymentKeyboard.DATA_CHECK
            ),
            InlineKeyboardButton(
                text="Отмена", callback_data=PaymentKeyboard.DATA_CANCEL
            ),
        )
        keyboard.add(InlineKeyboardButton(text="Перейти оплатить", url=url))

        return keyboard.as_markup()
