from sqlalchemy import BigInteger, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ReferLink(Base):
    __tablename__ = "promo_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    bonus: Mapped[float] = mapped_column(Float, nullable=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=False
    )
    referrer_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=True
    )
    link_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    user = relationship("User", back_populates="refer_links", foreign_keys=[user_id])
    referrer = relationship(
        "User", back_populates="referred_links", foreign_keys=[referrer_id]
    )
