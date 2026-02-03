from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.models import User as DBUser


class UserKeyboards:
    DATA_HOME_MENU = "HOME_MENU"

    # /start
    DATA_USER_INFO_MENU = "USER_INFO_MENU"
    DATA_GENERATE_VIDEO = "GENERATE_VIDEO"

    # Личный кабинет
    DATA_USER_INFO = "USER_INFO"
    DATA_USER_UP_BALANCE = "USER_UP_BALANCE"
    DATA_USER_REFERRAL = "USER_REFERRAL"

    DATA_CHECK_PAYMENT = "CHECK_PAYMENT"
    DATA_CANCEL_PAYMENT = "CANCEL_PAYMENT"

    PREFIX_REFERRAL = "REFERRAL:"

    @staticmethod
    def back_to(to: str) -> InlineKeyboardMarkup:
        """Возвращает кнопку 'Назад' с callback_data=to"""
        buttons = InlineKeyboardBuilder()
        buttons.row(InlineKeyboardButton(text="Назад", callback_data=to))
        return buttons.as_markup()

    @staticmethod
    def home_menu() -> InlineKeyboardMarkup:
        """/start Главное меню"""
        buttons = InlineKeyboardBuilder()
        buttons.row(
            InlineKeyboardButton(
                text="Личный кабинет", callback_data=UserKeyboards.DATA_USER_INFO_MENU
            ),
        )
        buttons.row(
            InlineKeyboardButton(
                text="Генерация Видео", callback_data=UserKeyboards.DATA_GENERATE_VIDEO
            )
        )
        return buttons.as_markup()

    @staticmethod
    def user_info_menu(back_to: str) -> InlineKeyboardMarkup:
        """Личный кабинет или callback data DATA_USER_INFO_MENU"""
        buttons = InlineKeyboardBuilder()
        buttons.row(
            InlineKeyboardButton(
                text="Мой профиль", callback_data=UserKeyboards.DATA_USER_INFO
            )
        )
        buttons.row(
            InlineKeyboardButton(
                text="Пополнить баланс",
                callback_data=UserKeyboards.DATA_USER_UP_BALANCE,
            )
        )
        buttons.row(
            InlineKeyboardButton(
                text="Реферальная программа",
                callback_data=UserKeyboards.DATA_USER_REFERRAL,
            )
        )
        buttons.row(InlineKeyboardButton(text="Назад", callback_data=back_to))
        return buttons.as_markup()

    @staticmethod
    def referals_button(users: list[DBUser], back_to: str) -> InlineKeyboardMarkup:
        """Кнопка рефералов"""
        buttons = InlineKeyboardBuilder()
        for user in users:
            buttons.row(
                InlineKeyboardButton(
                    text=f"{user.username}",
                    callback_data=UserKeyboards.PREFIX_REFERRAL + str(user.id),
                )
            )
        buttons.row(InlineKeyboardButton(text="Назад", callback_data=back_to))
        return buttons.as_markup()

    @staticmethod
    def payment_keyboard(url: str) -> InlineKeyboardMarkup:
        """Кнопка оплаты"""
        buttons = InlineKeyboardBuilder()
        buttons.row(
            InlineKeyboardButton(
                text="Проверить оплату", callback_data=UserKeyboards.DATA_CHECK_PAYMENT
            ),
            InlineKeyboardButton(
                text="Отменить оплату", callback_data=UserKeyboards.DATA_CANCEL_PAYMENT
            ),
            InlineKeyboardButton(text="Перейти и оплатить", url=url),
        )
        buttons.adjust(2)
        return buttons.as_markup()
