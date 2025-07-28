import aioredis
from fastapi import HTTPException


class RedisUserRepository:

    def __init__(self, redis_url: str):
        self.redis = aioredis.from_url(redis_url, decode_responses=True)

    async def set_refresh_token(self, user_id: int, refresh_token: str):
        await self.redis.set(f"refresh_token:{user_id}", refresh_token)

    async def get_refresh_token(self, user_id: int):
        token = await self.redis.get(f"refresh_token:{user_id}")
        if token is None:
            raise HTTPException(status_code=404, detail="Token not found")
        return token

    async def delete_refresh_token(self, user_id: int):
        await self.redis.delete(f"refresh_token:{user_id}")
