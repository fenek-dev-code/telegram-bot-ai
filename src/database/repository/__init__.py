"""This is a repository module for the telegram-bot-ai project."""

from .refer_link import ReferLinkRepository
from .transaction import TransactionRepository
from .user import UserRepository


class Repository:
    def __init__(self, session):
        self.user = UserRepository(session)
        self.transaction = TransactionRepository(session)
        self.refer_link = ReferLinkRepository(session)


__all__ = ["Repository"]
