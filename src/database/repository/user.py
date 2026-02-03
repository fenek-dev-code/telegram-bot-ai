from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.user import User
from src.pkg.logger import log


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: User) -> User | None:
        try:
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
            user = (
                await self.session.execute(select(User).where(User.id == telegram_id))
            ).scalar_one_or_none()
            if user and user.banned is not None:
                raise Exception("User is banned")
            return user

        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Failed to get user: {e}")
            return None
        except Exception as e:
            log.error(f"Failed to get user: {e}")
            return None

    async def update_user(self, telegram_id: int, **kwargs) -> User | None:
        try:
            user = await self.session.get(User, telegram_id)
            if user:
                if user.banned is not None:
                    raise Exception("User is banned")
                for key, value in kwargs.items():
                    setattr(user, key, value)
                await self.session.commit()
                await self.session.refresh(user)

                return user
            else:
                log.error(f"User with ID {telegram_id} not found")
                raise Exception(f"User with ID {telegram_id} not found")
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Failed to update user: {e}")
            raise Exception(f"Failed to update user: {e}")
        except Exception as e:
            log.error(f"Failed to update user: {e}")
            raise Exception(f"Failed to update user: {e}")

    async def get_user_by_ref_code(self, ref_code: str) -> User | None:
        """Берём пользователя по реф коду что бы понять валидный ли код"""
        try:
            return (
                await self.session.execute(
                    select(User).where(User.referral_code == ref_code)
                )
            ).scalar_one_or_none()
        except Exception as e:
            log.error(f"Failed to update user: {e}")
            raise Exception(f"Failed to update user: {e}")

    async def get_users_by_refer_id(self, id: int) -> list[User]:
        try:
            result = (
                (await self.session.execute(select(User).where(User.referrer_id == id)))
                .scalars()
                .all()
            )
            return list(result)
        except Exception as err:
            log.error(err)
            raise Exception("Ошибка при получении пользователей")

    async def get_user_with_deps(self, id: int) -> User | None:
        return (
            await self.session.execute(
                select(User)
                .where(User.id == id)
                .options(selectinload(User.transactions), selectinload(User.videos))
            )
        ).scalar_one_or_none()

    async def close_session(self):
        await self.session.close()
