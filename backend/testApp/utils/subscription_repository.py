from abc import ABC, abstractmethod

from sqlalchemy import select, insert, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from models.subscription import Subscription, SubscriptionStatus
from models.user import User


class AbstractSubscriptionRepository(ABC):

    @abstractmethod
    async def create(
        self,
        subscriber_id: int,
        target_id: int,
        session: AsyncSession,
        status: SubscriptionStatus = SubscriptionStatus.ACTIVE,
    ) -> Subscription:
        raise NotImplementedError

    @abstractmethod
    async def get(
        self, subscriber_id: int, target_id: int, session: AsyncSession
    ) -> Optional[Subscription]:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self, subscriber_id: int, target_id: int, session: AsyncSession
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_subscribers(
        self, user_id: int, session: AsyncSession
    ) -> List[Subscription]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_subscriptions(
        self, user_id: int, session: AsyncSession
    ) -> List[Subscription]:
        raise NotImplementedError

    @abstractmethod
    async def get_subscribers_count(self, user_id: int, session: AsyncSession) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_subscriptions_count(self, user_id: int, session: AsyncSession) -> int:
        raise NotImplementedError


class SQLAlchemySubscriptionRepository(AbstractSubscriptionRepository):

    model = Subscription

    async def create(
        self,
        subscriber_id: int,
        target_id: int,
        session: AsyncSession,
        status: SubscriptionStatus = SubscriptionStatus.ACTIVE,
    ) -> Subscription:
        subscription_data = {
            "subscriber_id": subscriber_id,
            "target_id": target_id,
            "status": status,
        }

        async with session.begin():
            stmt = insert(self.model).values(**subscription_data).returning(self.model)
            result = await session.execute(stmt)
            subscription = result.scalar_one()

            stmt = (
                update(User)
                .where(User.id == subscriber_id)
                .values(subscriptions_count=User.subscriptions_count + 1)
            )
            await session.execute(stmt)

            stmt = (
                update(User)
                .where(User.id == target_id)
                .values(subscribers_count=User.subscribers_count + 1)
            )
            await session.execute(stmt)

            return subscription

    async def get(
        self, subscriber_id: int, target_id: int, session: AsyncSession
    ) -> Optional[Subscription]:
        async with session.begin():
            stmt = select(self.model).where(
                (self.model.subscriber_id == subscriber_id)
                & (self.model.target_id == target_id)
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def delete(
        self, subscriber_id: int, target_id: int, session: AsyncSession
    ) -> None:
        async with session.begin():
            stmt = delete(self.model).where(
                (self.model.subscriber_id == subscriber_id)
                & (self.model.target_id == target_id)
            )
            await session.execute(stmt)
            stmt = (
                update(User)
                .where(User.id == subscriber_id)
                .values(subscriptions_count=User.subscriptions_count - 1)
            )
            await session.execute(stmt)

            stmt = (
                update(User)
                .where(User.id == target_id)
                .values(subscribers_count=User.subscribers_count - 1)
            )
            await session.execute(stmt)

    async def get_user_subscribers(
        self, user_id: int, session: AsyncSession
    ) -> List[Subscription]:
        async with session.begin():
            stmt = select(self.model).where(
                (self.model.subscriber_id == user_id)
                & (self.model.status == SubscriptionStatus.ACTIVE)
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_user_subscribers_id(
        self, user_id: int, session: AsyncSession
    ) -> List[int]:
        async with session.begin():
            stmt = select(self.model.target_id).where(
                (self.model.subscriber_id == user_id)
                & (self.model.status == SubscriptionStatus.ACTIVE)
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_user_subscriptions(
        self, user_id: int, session: AsyncSession
    ) -> List[Subscription]:
        async with session.begin():
            stmt = select(self.model).where(
                (self.model.subscriber_id == user_id)
                & (self.model.status == SubscriptionStatus.ACTIVE)
            )
            subscriptions = await session.execute(stmt)
            result = subscriptions.scalars().all()
            return result

    async def get_subscribers_count(self, user_id: int, session: AsyncSession) -> int:
        async with session.begin():
            stmt = select(func.count()).where(
                (self.model.target_id == user_id)
                & (self.model.status == SubscriptionStatus.ACTIVE)
            )
            result = await session.execute(stmt)
            return result.scalar_one() or 0

    async def get_subscriptions_count(self, user_id: int, session: AsyncSession) -> int:
        async with session.begin():
            stmt = select(func.count()).where(
                (self.model.subscriber_id == user_id)
                & (self.model.status == SubscriptionStatus.ACTIVE)
            )
            result = await session.execute(stmt)
            return result.scalar_one() or 0

    async def update_status(
        self,
        subscriber_id: int,
        target_id: int,
        session: AsyncSession,
        new_status: SubscriptionStatus,
    ) -> Optional[Subscription]:
        async with session.begin():
            existing = await self.get(subscriber_id, target_id, session)
            if not existing:
                return None

            stmt = (
                update(self.model)
                .where(
                    (self.model.subscriber_id == subscriber_id)
                    & (self.model.target_id == target_id)
                )
                .values(status=new_status)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            return result.scalar_one()

    async def get_pending_subscriptions(
        self, user_id: int, session: AsyncSession
    ) -> List[Subscription]:
        async with session.begin():
            stmt = select(self.model).where(
                (self.model.target_id == user_id)
                & (self.model.status == SubscriptionStatus.PENDING)
            )
            result = await session.execute(stmt)
            return list(result.scalars().all())
