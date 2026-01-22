from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class ReferLink(Base):
    __tablename__ = "promo_links"

    name = Column(String(100), unique=True, nullable=False)
    bonus = Column(Float, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=True)
    link_code = Column(String(50), unique=True, nullable=False)

    # Связи
    # Убрана ссылка на несуществующую модель PromoStat. Добавьте её при необходимости.
    user = relationship("User", back_populates="refer_links", foreign_keys=[user_id])
    referrer = relationship(
        "User", back_populates="referred_links", foreign_keys=[referrer_id]
    )
    admin = relationship("Admin", back_populates="created_links")
