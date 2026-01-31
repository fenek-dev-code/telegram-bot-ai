from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Admin(Base):
    __tablename__ = "admins"
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        nullable=False,
        comment="ID пользователя в Telegram (первичный ключ)",
    )
    created_links = relationship("ReferLink", back_populates="admin")
