from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import ReferLink
from src.pkg.logger import log


class ReferLinkRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def create_poromo_link(self):
        pass

    async def get_promo_link(self, ref_code: str) -> ReferLink | None:
        if ref_code == "":
            return None
        return (
            await self.session.execute(
                select(ReferLink).where(ReferLink.link_code == ref_code)
            )
        ).scalar_one_or_none()
