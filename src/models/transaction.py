from enum import Enum

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class PaymentStatus(Enum):
    """Status of generated content."""

    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Transaction(Base):
    __tablename__ = "transactions"
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    status = Column(String(30), default=PaymentStatus.PROCESSING)

    # Связи
    user = relationship("User", back_populates="transactions")
