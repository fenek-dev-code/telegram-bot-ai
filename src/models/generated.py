from enum import Enum

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class GeneratedStatus(Enum):
    """Status of generated content."""

    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class GenerateFormat(Enum):
    """Formats for generated content."""

    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"


class Generated(Base):
    __tablename__ = "converted_videos"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(30), default=GeneratedStatus.PROCESSING)
    format: Mapped[str] = mapped_column(String(30), default=GenerateFormat.VIDEO)
    time_duration: Mapped[float] = mapped_column(Float, nullable=True)
    amount_tokens: Mapped[float] = mapped_column(Float, nullable=True)

    # Связи
    user = relationship("User", back_populates="videos")
