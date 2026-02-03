from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Transaction
from src.pkg.logger import log


class TransactionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_transaction(
        self, user_id: int, amount: float, type: str
    ) -> Transaction | None:
        try:
            transaction = Transaction(user_id=user_id, amount=amount, type=type)
            self.session.add(transaction)
            await self.session.commit()
            await self.session.refresh(transaction)
            return transaction
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Error creating transaction: {e}")
        return None

    async def update_transaction(
        self, transaction_id: int, status: str
    ) -> Transaction | None:
        try:
            transaction = await self.session.get(Transaction, transaction_id)
            if transaction:
                transaction.status = status
                await self.session.commit()
                await self.session.refresh(transaction)
                return transaction
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Error updating transaction: {e}")
        return None

    async def get_transactions_by_user_id(
        self, user_id: int, payment_type: str | None = None
    ) -> list[Transaction]:
        """
        Получение транзакций пользователя (read-only операция)
        """
        try:
            query = select(Transaction).where(Transaction.user_id == user_id)
            if payment_type:
                query = query.where(Transaction.type == payment_type)
            result = await self.session.scalars(query)
            return list(result.all())  # Явно приводим к list
        except SQLAlchemyError as e:
            log.error(f"Error getting transactions for user {user_id}: {e}")
            return []
