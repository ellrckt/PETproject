from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from utils.subscription_repository import AbstractSubscriptionRepository
from redis_service.redis_profile_service import RedisJSONProfileService
from repository.subscription import SubscriptionRepository
from models.subscription import Subscription
from models.profiles import Profile
from auth.utils import decode_jwt


class SubscriptionService:

    def __init__(self, subscription_repository: AbstractSubscriptionRepository):

        self.subscription_repository = subscription_repository()

    async def subscribe(
        self, refresh_token: str, target_id: int, session: AsyncSession
    ) -> Subscription:
        payload = decode_jwt(refresh_token)
        subscriber_id = payload["user_id"]
        existing = await self.subscription_repository.get(
            subscriber_id, target_id, session
        )
        if existing:
            raise HTTPException(status_code=400, detail="Already subscribed")

        return await self.subscription_repository.create(
            subscriber_id, target_id, session
        )

    async def unsubscribe(
        self, refresh_token: str, target_id: int, session: AsyncSession
    ) -> Subscription:
        payload = decode_jwt(refresh_token)
        subscriber_id = payload["user_id"]
        existing = await self.subscription_repository.get(
            subscriber_id, target_id, session
        )
        if not existing:
            raise HTTPException(status_code=400, detail="Not subscribed")

        return await self.subscription_repository.delete(
            subscriber_id, target_id, session
        )

    async def get_subscribers_with_info(
        self, user_id: int, session: AsyncSession
    ) -> List[dict]:
        subscriptions = await self.subscription_repository.get_user_subscribers(
            user_id, session
        )

        return [
            {
                "subscriber_id": sub.subscriber_id,
                "status": sub.status.value,
                "created_at": sub.created_at,
            }
            for sub in subscriptions
        ]

    async def get_subscriptions(self, refresh_token: str, session: AsyncSession):

        payload = decode_jwt(refresh_token)
        user_id = payload["user_id"]
        result = await self.subscription_repository.get_user_subscriptions(
            user_id, session
        )
        return result

    async def get_subscribers_profiles(
        self,
        refresh_token: str,
        profile_service: Profile,
        redis_json_service: RedisJSONProfileService,
        session: AsyncSession,
    ) -> List[Profile]:
        payload = decode_jwt(refresh_token)
        user_id = payload["user_id"]
        user_subscribers = await self.subscription_repository.get_user_subscribers_id(
            user_id, session
        )
        result = await profile_service.get_user_profiles(
            user_subscribers, redis_json_service, session
        )
        return result
