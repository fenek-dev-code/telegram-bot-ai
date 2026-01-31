from aiogram.types import User as TgUser

from src.models import GeneratedStatus, PaymentStatus, User


class ReplyMessages:
    MESSAGE_START: str = "Message Start\n" + ""

    @staticmethod
    def start_message(user: User) -> str:
        return (
            f"Здравствуйте {user.username}\n"
            + f"Ваш баланс {user.balance}\n"
            + f"Вы зарегестрированны {user.created_at}"
        )

    @staticmethod
    def referals_message(user_name: str, have_referals: bool, ref_link: str) -> str:
        base_message = (
            f"Приветсвую {user_name} !\n"
            + "Реферальнная программа - с каждого приглашонного пользователя ты получаешь 5% от его пополнений!\n"
        )

        if not have_referals:
            return (
                base_message
                + "Вижу у тебя пока нет рефералов но ты всегда можешь их приглостить \n"
                + ref_link
            )
        return (
            base_message
            + "Твои рефералы ниже списком тыкни что бы увидить подробнее!\n"
            + ref_link
        )

    @staticmethod
    def referal_info(user: User) -> str:
        builder = f"Реферал: {user.username}\n"
        amount: float = 0
        balanc_count: int = 0
        videos: int = 0
        for i in user.transactions:
            if i.status == PaymentStatus.COMPLETED:
                amount += i.amount
                balanc_count += 1
        for i in user.videos:
            if i.status == GeneratedStatus.COMPLETED:
                videos += 1

        builder += f"Генераций: {videos}\n"
        builder += f"Пополнений: {balanc_count}\n"
        builder += f"Сумма пополнений: {amount}\n"
        builder += f"Вы получили: {amount / 100 * 5}"
        return builder

    @staticmethod
    def generate_video() -> str:
        return "Опишите промт или прешлите фото с промтом для генерации видео!"

    @staticmethod
    def generate_image() -> str:
        return "Опишите промт или прешлите фото с промтом для генерации изображения!"

    @staticmethod
    def up_balance(user: TgUser) -> str:
        name: str
        if user.full_name:
            name = user.full_name
        elif user.username:
            name = user.username
        else:
            name = "Дорогой пользователь"
        return (
            f"{name}, для пополнения баланса отправьте сумму пополнения например - 249"
        )
