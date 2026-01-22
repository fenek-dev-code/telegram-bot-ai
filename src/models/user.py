from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    balance = Column(Float, default=0.0)

    invited_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    referral_code = Column(String(50), unique=True, nullable=True)
    banned = Column(Boolean, default=False)

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
