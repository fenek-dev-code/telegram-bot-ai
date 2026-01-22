from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from src.database import Base


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False)

    created_links = relationship("PromoLink", back_populates="admin")
