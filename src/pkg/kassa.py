import uuid

from yookassa import Configuration, Payment
from yookassa.payment import PaymentResponse

from src.config import config

Configuration.account_id = config.YOOKASSA_ID
Configuration.secret_key = config.YOOKASSA_KEY


def create_payment(count: float, user_id: int) -> PaymentResponse:
    return Payment.create(
        {
            "amount": {"value": f"{count}", "currency": "RUB"},
            "capture": True,
            "description": f"Заказ пользователя ID: {user_id}",
            "confirmation": {
                "type": "redirect",
                "return_url": "https://www.example.com/return_url",
            },
            "test": (config.PROD == False),
        },
        uuid.uuid4(),
    )
