from enum import Enum

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Format(Enum):
    """Formats for generated content."""

    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"


class Generated(Base):
    __tablename__ = "converted_videos"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="processing")  # processing, completed, failed
    format = Column(String(10), default="video")  # video, audio, image
    time_duration = Column(Float, nullable=True)
    amount_tokens = Column(Float, nullable=True)

    # Связи
    user = relationship("User", back_populates="videos")
