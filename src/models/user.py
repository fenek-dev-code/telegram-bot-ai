import uuid
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from . import Generated, ReferLink, Transaction


class User(Base):
    __tablename__ = "users"

    # ВАЖНО: Добавьте primary key
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=True)
    balance: Mapped[float] = mapped_column(Float, default=0.0)
    referrer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    referral_code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
        index=True,
        default=lambda: str(uuid.uuid4())[:8].upper(),
    )
    banned: Mapped[bool | None] = mapped_column(Boolean, default=None)

    # Связи
    # Self-referential relationship
    referrer: Mapped["User"] = relationship(
        "User",
        remote_side=[id],  # Теперь используем id текущей модели
        foreign_keys=[referrer_id],
        back_populates="referrals",  # Связываем с back_populates
        uselist=False,  # У одного пользователя только один реферер
    )

    # Уберите дублирующее определение! Оставьте только одно
    referrals: Mapped[list["User"]] = relationship(
        "User",
        back_populates="referrer",  # Обратная связь
        foreign_keys=[referrer_id],  # Важно указать foreign_keys здесь тоже
        cascade="all, delete-orphan",
        lazy="dynamic",  # Или "select" если не нужен dynamic query
    )

    # Ссылки и связанные объекты
    refer_links: Mapped[list["ReferLink"]] = relationship(
        "ReferLink", back_populates="user", foreign_keys="ReferLink.user_id"
    )

    referred_links: Mapped[list["ReferLink"]] = relationship(
        "ReferLink", back_populates="referrer", foreign_keys="ReferLink.referrer_id"
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="user"
    )

    videos: Mapped[list["Generated"]] = relationship("Generated", back_populates="user")

    def generate_referral_link(self, bot_username: str) -> str:
        """Генерация реферальной ссылки"""
        return f"https://t.me/{bot_username}?start={self.referral_code}"
