from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Admin(Base):
    __tablename__ = "admins"

    user_id: Mapped[int] = mapped_column(
        Integer, unique=True, nullable=False, index=True
    )

    created_links = relationship("ReferLink", back_populates="admin")
