from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        Integer, unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(String, nullable=True)
    balance: Mapped[float] = mapped_column(Float, default=0.0)

    invited_by: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    referral_code: Mapped[str | None] = mapped_column(
        String(50), unique=True, nullable=True
    )
    banned: Mapped[bool | None] = mapped_column(Boolean, default=None)

    # Связи
    # Self-referential relationship — remote_side должен ссылаться на PK (id).
    referrer = relationship("User", remote_side=[Base.id], back_populates="referrals")
    referrals = relationship("User", back_populates="referrer")

    # Ссылки и связанные объекты
    refer_links = relationship(
        "ReferLink", back_populates="user", foreign_keys="ReferLink.user_id"
    )
    referred_links = relationship(
        "ReferLink", back_populates="referrer", foreign_keys="ReferLink.referrer_id"
    )

    transactions = relationship("Transaction", back_populates="user")
    videos = relationship("Generated", back_populates="user")
