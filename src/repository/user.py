from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.pkg.logger import log


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, **kwargs) -> User | None:
        try:
            user = User(**kwargs)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Failed to create user: {e}")
            raise Exception(f"Failed to create user: {e}")
        except Exception as e:
            log.error(f"Failed to create user: {e}")
            raise Exception(f"Failed to create user: {e}")

    async def get_user(self, telegram_id: int) -> User | None:
        try:
            user = await self.session.get(User, telegram_id)
            if user and user.banned is not None:
                raise Exception("User is banned")
            return user
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Failed to get user: {e}")
            raise Exception(f"Failed to get user: {e}")
        except Exception as e:
            log.error(f"Failed to get user: {e}")
            raise Exception(f"Failed to get user: {e}")

    async def update_user(self, user_id: int, **kwargs) -> User | None:
        try:
            user = await self.session.get(User, user_id)
            if user:
                if user.banned is not None:
                    raise Exception("User is banned")
                for key, value in kwargs.items():
                    setattr(user, key, value)
                await self.session.commit()
                await self.session.refresh(user)

                return user
            else:
                log.error(f"User with ID {user_id} not found")
                raise Exception(f"User with ID {user_id} not found")
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Failed to update user: {e}")
            raise Exception(f"Failed to update user: {e}")
        except Exception as e:
            log.error(f"Failed to update user: {e}")
            raise Exception(f"Failed to update user: {e}")

    async def close_session(self):
        await self.session.close()
