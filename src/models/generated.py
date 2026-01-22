from enum import Enum

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

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

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(String(30), default=GeneratedStatus.PROCESSING)
    format = Column(String(30), default=GenerateFormat.VIDEO)
    time_duration = Column(Float, nullable=True)
    amount_tokens = Column(Float, nullable=True)

    # Связи
    user = relationship("User", back_populates="videos")
