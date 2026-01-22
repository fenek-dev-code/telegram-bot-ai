from enum import Enum

from .admin import Admin
from .generated import Generated
from .transaction import Transaction
from .user import User


class Status(Enum):
    """Status of generated content."""

    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


__all__ = ["User", "Admin", "Generated", "Transaction", "Status"]
