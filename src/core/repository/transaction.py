from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Transaction
from src.pkg.logger import log


class TransactionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_transaction(
        self, user_id: int, amount: float
    ) -> Transaction | None:
        try:
            transaction = Transaction(
                user_id=user_id, amount=amount, status="completed"
            )
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
