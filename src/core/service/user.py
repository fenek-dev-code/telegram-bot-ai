from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repository import (
    ReferLinkRepository,
    TransactionRepository,
    UserRepository,
)
from src.models import User


class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)
        self.promoRepo = ReferLinkRepository(session)
        self.repoTr = TransactionRepository(session)

    async def create_user(
        self, id: int, ref_code: str = "", username: str | None = None
    ) -> User | None:
        if ref_code != "":
            ref_bonus = await self.promoRepo.get_promo_link(ref_code)
            if ref_bonus:
                return await self.repo.create_user(
                    User(
                        id=id,
                        username=username,
                        balance=ref_bonus.bonus,
                        referrer_id=ref_bonus.id,
                    )
                )
            ref_user = await self.repo.get_user_by_ref_code(ref_code)
            if ref_user:
                return await self.repo.create_user(
                    User(
                        id=id,
                        username=username,
                        referrer_id=ref_user.id,
                    )
                )
        return await self.repo.create_user(User(id=id, username=username))

    async def get_referal_users(self, id: int) -> list[User]:
        return await self.repo.get_users_by_refer_id(id)

    async def get_user(self, id: int) -> User | None:
        return await self.repo.get_user(id)

    async def get_user_stat(self, id: int) -> User | None:
        return await self.repo.get_user_with_deps(id)

    async def update_user_balance(self, id: int, amount: float):
        user = await self.repo.update_user(id, balance=amount)
        if user:
            await self.repoTr.create_transaction(id, amount)
            referal_cent = (amount / 100) * 5
            await self.repo.update_user(user.referrer_id, balance=referal_cent)
