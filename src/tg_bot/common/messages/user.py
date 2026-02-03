from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from src.database.models import PaymentType, Transaction
    from src.database.models import User as DBUser


class UserMessages:
    """Сообщения для пользователя"""

    MESSAGE_START: str = (
        "🎉 Добро пожаловать в AIVideos\n\n"
        + "Первый бот создающий из фотографий полноценные ии видео неотличимое от реального."
    )

    MESSAGE_USER_INFO_MENU: str = (
        "Привет дорогой друг, это твой личный профиль, здесь ты сможешь:\n"
        + "посмотреть свою статистику, пополнить баланс, пригласить своих друзей"
    )

    MESSAGE_GENERATE_VIDEO: str = (
        "Здесь вы можете создать свое видео, отправьте фото модели!\n"
        + "Перед отправкой фото, посмотрите обучающее видео\n"
    )

    MESSAGE_REFERAL: str = (
        "Пригласи друзей и получай бонусы!\n"
        + "Каждый новый пользователь, который пришел по твоей ссылке, дает тебе бонусы."
    )

    @staticmethod
    def referals_message(
        botname: str,
        referal_code: str,
        referal_count: int,
        transactions: list[Transaction],
    ) -> str:
        ref_link = f"https://t.me/{botname}?start={referal_code}"
        amount = sum(transaction.amount for transaction in transactions)
        return (
            "Ты можешь пригласить друзей и получать бонусы!\n"
            + "Каждый новый пользователь, который пришел по твоей ссылке, дает тебе бонусы.\n"
            + f"Уже приглашеные: {referal_count}\n"
            + f"Сумма бонусов: {amount} руб.\n"
            + f"<a href='{ref_link}'>Ссылка для приглашения</a>"
        )

    @staticmethod
    def message_referal_info(referal: DBUser) -> str:
        amount = sum(transaction.amount for transaction in referal.transactions)
        return (
            f"Твой приглашённый пользователь: {referal.username}\n"
            + f"Генераций: {len(referal.videos)}\n"
            + f"Сумма пополнений: {amount} руб.\n"
            + f"Сумма бонусов: {amount / 100 * 5} руб.\n"
        )

    @staticmethod
    def message_user_info(user: DBUser) -> str:
        amount = sum(transaction.amount for transaction in user.transactions)
        bonus = sum(
            transaction.amount
            for transaction in user.transactions
            if transaction.type == PaymentType.REFERRAL
        )
        return (
            f"Твой пользователь: {user.username}\n"
            + f"Генераций: {len(user.videos)}\n"
            + f"Сумма пополнений: {amount:.2f} руб.\n"
            + f"Сумма бонусов: {bonus:.2f} руб.\n"
        )
