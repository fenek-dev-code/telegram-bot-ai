from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
)

# from sqlalchemy.orm import relationship
from src.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    balance = Column(Float, default=0.0)

    invited_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    referral_code = Column(String(50), unique=True, nullable=True)
    banned = Column(Boolean, default=False)

    # # Связи
    # referrer = relationship("User", remote_side=[id], backref="referrals")
    # promo_link = relationship("PromoLink", backref="users")
    # transactions = relationship("Transaction", back_populates="user")
    # videos = relationship("ConvertedVideo", back_populates="user")
