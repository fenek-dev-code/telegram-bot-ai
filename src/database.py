from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import declarative_base

base = declarative_base()


class Base(base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
