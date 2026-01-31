from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.models import User

from .call_back_data import CallBackData as Data


class UserButtons:
    @staticmethod
    def get_home_menu() -> InlineKeyboardMarkup:
        buttons = InlineKeyboardBuilder()
        buttons.row(
            InlineKeyboardButton(
                text="Реферальная программа", callback_data=Data.REFERAL_SYSTEM
            ),
            InlineKeyboardButton(
                text="Пополнить баланс", callback_data=Data.UP_BALANCE
            ),
        )
        buttons.row(
            InlineKeyboardButton(
                text="Генерация Видео", callback_data=Data.GENERATE_VIDEO
            ),
            InlineKeyboardButton(
                text="Генерация Изображения", callback_data=Data.GENERATE_IMAGE
            ),
        )
        return buttons.as_markup()

    @staticmethod
    def referals_button(users: list[User]) -> InlineKeyboardMarkup:
        buttons = InlineKeyboardBuilder()
        for user in users:
            buttons.row(
                InlineKeyboardButton(
                    text=user.username,
                    callback_data=f"{Data.REFERAL_USER_PREFIX}{user.id}",
                )
            )
        buttons.row(InlineKeyboardButton(text="Назад", callback_data=Data.START))
        return buttons.as_markup()

    @staticmethod
    def go_home() -> InlineKeyboardMarkup:
        buttons = InlineKeyboardBuilder()
        buttons.row(InlineKeyboardButton(text="Назад", callback_data=Data.START))
        return buttons.as_markup()


class PaymentButtons:
    @staticmethod
    def check_payment_status(url: str) -> InlineKeyboardMarkup:
        buttons = InlineKeyboardBuilder()
        buttons.row(InlineKeyboardButton(text="Отменить", callback_data=Data.START))
        buttons.row(
            InlineKeyboardButton(
                text="Оплатил", callback_data=Data.PAYMENT_CHECK_STATUS
            )
        )
        buttons.row(InlineKeyboardButton(text="Перейти и оплатить", url=url))
        return buttons.as_markup()
