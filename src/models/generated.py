from enum import Enum

from sqlalchemy import BigInteger, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class GeneratedStatus(Enum):
    """Status of generated content."""

    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Generated(Base):
    __tablename__ = "converted_videos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(30), default=GeneratedStatus.PROCESSING)
    prompt: Mapped[str] = mapped_column(Text, nullable=True)

    time_duration: Mapped[float] = mapped_column(Float, nullable=True)
    amount_tokens: Mapped[float] = mapped_column(Float, nullable=True)

    # Связи
    user = relationship("User", back_populates="videos")
