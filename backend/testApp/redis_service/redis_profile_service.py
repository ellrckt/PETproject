import redis.asyncio as redis
from redis.commands.json.path import Path
import os
from typing import Optional, Dict, Any, List, Set
import logging
from dotenv import load_dotenv
import json
from datetime import datetime
from models.profiles import Profile

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class RedisJSONProfileService:
    def __init__(self):
        self.logger = logging.getLogger("redis_service")
        self.logger.setLevel(logging.DEBUG)

        
        self.redis_host = os.getenv("REDIS_HOST", "redis")
        self.redis_port = int(os.getenv("REDIS_PORT", 6379))
        self.redis_db = int(os.getenv("REDIS_DB", 0))
        self.logger.debug(f"Redis host: {self.redis_host}")
        self.logger.debug(f"Redis port: {self.redis_port}")
        self.logger.debug(f"Redis db: {self.redis_db}")
        
        self.redis_client: Optional[redis.Redis] = None
        self.json_client = None
        self.channel_subscribers: Dict[str, Set[str]] = {}

    async def connect(self):
        if self.redis_client is not None:
            return 
            
        try:
            self.logger.debug(f"Connecting to Redis at {self.redis_host}:{self.redis_port}")
            
            self.redis_client = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                db=self.redis_db,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2,
                retry_on_timeout=False, 
            )
            
            await self.redis_client.ping()
            
            self.json_client = self.redis_client.json()
            self.logger.info("Redis JSON client connected successfully")
            
        except redis.ConnectionError as e:
            self.logger.error(f"Redis connection failed: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected Redis error: {e}")

    async def _ensure_connected(self):
        if self.redis_client is None:
            await self.connect()

    # async def create_private_chat(
    #     self,
    #     user_id: str,
    #     room_name: Optional[str],
    # ):
    #     pass

    async def check_connection(self):
        try:
            await self.redis_client.ping()
            self.logger.debug("Redis is OK")
            return True
        except redis.ConnectionError:
            self.logger.debug("Failed to connect to Redis JSON")
            return False

    def _get_profile_key(self, user_id: str) -> str:
        return f"profile:user_{user_id}"

    def _get_profiles_key(self) -> str:
        return "profiles:all"

    def _get_room_key(self, room_id: str) -> str:
        return f"room:{room_id}"

    def _get_rooms_key(self) -> str:
        return "rooms:all"

    # async def create_room(self, room_id: str):
    #     key = self._get_room_key(room_id)
    #     try:
    #         await self.json_client.set(key, Path.root_path(), {"created_at": datetime.now().isoformat()})
    #         await self.redis_client.sadd(self._get_profiles_key(), room_id)

    async def create_profile(
        self,
        user_id: str,
        profile_data: Dict[str, Any],
        expire_seconds: Optional[int] = None,
    ) -> bool:
        print(f"🔥 REDIS DEBUG: create_profile called! user_id={user_id}, type={type(user_id)}")
        print(f"🔥 REDIS DEBUG: profile_data={profile_data}")
        print(f"🔥 REDIS DEBUG: redis_client={self.redis_client}, json_client={self.json_client}")
    
        await self._ensure_connected() 
        if self.redis_client is None:
            self.logger.info("Redis unavailable, skipping profile creation in cache")
            return False 
        try:
            key = self._get_profile_key(user_id)
            await self.json_client.set(
                key, Path.root_path(), profile_data
            )
            await self.redis_client.sadd(self._get_profiles_key(), str(user_id))
            return True
        except Exception as e:
            self.logger.info(f"Error creating profile: {e}")
            return False

    async def create_profiles_pipeline(self, profiles: List[Profile]):
        await self._ensure_connected()
        
        if self.redis_client is None:
            return False
        async with self.redis_client.pipeline() as pipe:
            for profile in profiles:
                key = f"profile:{profile.user_id}"
                pipe.setex(key, self.expire_time, profile)
            await pipe.execute()

    async def get_profiles_pipeline(self, user_ids: List[int]) -> List[Optional[dict]]:
        keys = [self._get_profile_key(user_id) for user_id in user_ids]
        with self.json_client.pipeline() as pipe:
            for key in keys:
                pipe.get(key)
            results = await pipe.execute()
        decoded_results = []
        for result in results:
            if result is None:
                decoded_results.append(None)
            else:
                decoded_results.append(json.loads(result))

        return decoded_results

    async def get_profile(self, profile_id: str) -> Optional[Dict[str, Any]]:
        await self._ensure_connected()
        if self.redis_client is None or self.json_client is None:
            return None
        
        try:
            key = self._get_profile_key(profile_id)
            return await self.json_client.get(key)
        except Exception as e:
            self.logger.info(f"Error getting profile: {e}")
            return None

    async def get_profile_field(self, profile_id: str, field: str) -> Any:
        try:
            key = self._get_profile_key(profile_id)
            result = await self.json_client.get(key, f".{field}")
            return result
        except Exception as e:
            self.logger.infp(f"Error getting field {field}: {e}")
            return None

    async def update_profile(self, profile_id: str, updates: Dict[str, Any]) -> bool:
        await self._ensure_connected()
        
        if self.redis_client is None:
            return False
        try:
            key = self._get_profile_key(profile_id)
            if not await self.redis_client.exists(key):
                self.logger.info(f"Profile {key} does not exist")
                return False

            for field, value in updates.items():
                await self.json_client.set(key, f".{field}", value)

            return True
        except Exception as e:
            self.logger.info(f"Error updating profile: {e}")
            return False

    async def delete_profile(self, profile_id: str) -> bool:
        try:
            key = self._get_profile_key(profile_id)
            result = await self.redis_client.delete(key)
            await self.redis_client.srem(self._get_profiles_key(), profile_id)

            return result > 0
        except Exception as e:
            self.logger.info(f"Error deleting profile: {e}")
            return False

    async def get_all_profiles(self) -> List[Dict[str, Any]]:
        try:
            profile_ids = await self.redis_client.smembers(self._get_profiles_key())

            profiles = []
            for profile_id in profile_ids:
                profile = await self.get_profile(profile_id)
                if profile:
                    profiles.append({"id": profile_id, **profile})

            return profiles
        except Exception as e:
            self.logger.info(f"Error getting all profiles: {e}")
            return []

    async def search_profiles(self, field: str, value: Any) -> List[Dict[str, Any]]:
        try:
            all_profiles = await self.get_all_profiles()
            return [profile for profile in all_profiles if profile.get(field) == value]
        except Exception as e:
            self.logger.info(f"Error searching profiles: {e}")
            return []

    async def search_profiles_jsonpath(
        self, jsonpath_query: str
    ) -> List[Dict[str, Any]]:
        try:
            results = []
            profile_ids = await self.redis_client.smembers(self._get_profiles_key())

            for profile_id in profile_ids:
                key = self._get_profile_key(profile_id)
                try:
                    result = await self.json_client.get(key, jsonpath_query)
                    if result and result != []:
                        results.append({"id": profile_id, "data": result})
                except:
                    continue

            return results
        except Exception as e:
            self.logger.info(f"Error searching with JSONPath: {e}")
            return []

    async def profile_exists(self, profile_id: str) -> bool:
        return await self.redis_client.exists(self._get_profile_key(profile_id)) > 0

    async def get_profiles_count(self) -> int:
        try:
            return await self.redis_client.scard(self._get_profiles_key())
        except Exception as e:
            self.logger.info(f"Error getting profiles count: {e}")
            return 0

    async def clear_all_profiles(self) -> bool:
        try:
            keys = await self.redis_client.keys("profile:*")
            keys.append(self._get_profiles_key())

            if keys:
                await self.redis_client.delete(*keys)

            return True
        except Exception as e:
            self.logger.info(f"Error clearing profiles: {e}")
            return False
