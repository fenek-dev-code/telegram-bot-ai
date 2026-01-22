from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Transaction(Base):
    __tablename__ = "transactions"
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(20), default="pending")  # pending, completed, failed

    # Связи
    user = relationship("User", back_populates="transactions")
