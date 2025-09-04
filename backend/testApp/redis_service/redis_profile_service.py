import redis.asyncio as redis
from redis.commands.json.path import Path
import os
from typing import Optional, Dict, Any, List
import logging
from dotenv import load_dotenv

load_dotenv() 

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
class RedisJSONProfileService:
    def __init__(self):
        self.logger = logging.getLogger("redis_service")
        self.logger.setLevel(logging.DEBUG)
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        # redis_password = os.getenv('REDIS_PASSWORD', None)
        redis_db = int(os.getenv('REDIS_DB', 0))

        self.logger.debug(f"Redis host: {redis_host}")
        self.logger.debug(f"Redis port: {redis_port}")
        self.logger.debug(f"Redis db: {redis_db}")
        # self.logger.debug(f"Redis password: {redis_password}" if redis_password else "Redis password: [NOT SET]")

        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            # password=redis_password,
            decode_responses=True,
            socket_connect_timeout=5,
            retry_on_timeout=True
        )
        
        self.json_client = self.redis_client.json()
    
    async def check_connection(self):
        try:
            await self.redis_client.ping()
            self.logger.debug("Redis is OK")
            return True
        except redis.ConnectionError:
            self.logger.debug("Failed to connect to Redis JSON")
            return False
    
    def _get_profile_key(self, profile_id: str) -> str:
        return f"profile:user_{profile_id}"
    
    def _get_profiles_key(self) -> str:
        return "profiles:all"
    
    async def create_profile(self, profile_id: str, profile_data: Dict[str, Any], expire_seconds: Optional[int] = None) -> bool:
        try:
            key = self._get_profile_key(profile_id)
            await self.json_client.set(key, Path.root_path(), profile_data)            
            await self.redis_client.sadd(self._get_profiles_key(), profile_id)
            return True
        except Exception as e:
            self.logger.error(f"Error creating profile: {e}")
            return False
    
    async def get_profile(self, profile_id: str) -> Optional[Dict[str, Any]]:
        try:
            key = self._get_profile_key(profile_id)
            return await self.json_client.get(key)
        except Exception as e:
            self.logger.error(f"Error getting profile: {e}")
            return None
    
    async def get_profile_field(self, profile_id: str, field: str) -> Any:
        try:
            key = self._get_profile_key(profile_id)
            result = await self.json_client.get(key, f".{field}")
            return result
        except Exception as e:
            self.logger.error(f"Error getting field {field}: {e}")
            return None
    
    async def update_profile(self, profile_id: str, updates: Dict[str, Any]) -> bool:
        try:
            key = self._get_profile_key(profile_id)
            
            for field, value in updates.items():
                await self.json_client.set(key, f".{field}", value)
            
            return True
        except Exception as e:
            self.logger.error(f"Error updating profile: {e}")
            return False
    
    async def delete_profile(self, profile_id: str) -> bool:
        try:
            key = self._get_profile_key(profile_id)
            result = await self.redis_client.delete(key)
            await self.redis_client.srem(self._get_profiles_key(), profile_id)
            
            return result > 0
        except Exception as e:
            self.logger.error(f"Error deleting profile: {e}")
            return False
    
    async def get_all_profiles(self) -> List[Dict[str, Any]]:
        try:
            profile_ids = await self.redis_client.smembers(self._get_profiles_key())
            
            profiles = []
            for profile_id in profile_ids:
                profile = await self.get_profile(profile_id)
                if profile:
                    profiles.append({
                        'id': profile_id,
                        **profile
                    })
            
            return profiles
        except Exception as e:
            self.logger.error(f"Error getting all profiles: {e}")
            return []
    
    async def search_profiles(self, field: str, value: Any) -> List[Dict[str, Any]]:
        try:
            all_profiles = await self.get_all_profiles()
            return [profile for profile in all_profiles 
                   if profile.get(field) == value]
        except Exception as e:
            self.logger.error(f"Error searching profiles: {e}")
            return []
    
    async def search_profiles_jsonpath(self, jsonpath_query: str) -> List[Dict[str, Any]]:
        try:
            results = []
            profile_ids = await self.redis_client.smembers(self._get_profiles_key())
            
            for profile_id in profile_ids:
                key = self._get_profile_key(profile_id)
                try:
                    result = await self.json_client.get(key, jsonpath_query)
                    if result and result != []: 
                        results.append({
                            'id': profile_id,
                            'data': result
                        })
                except:
                    continue
            
            return results
        except Exception as e:
            self.logger.error(f"Error searching with JSONPath: {e}")
            return []
    
    async def profile_exists(self, profile_id: str) -> bool:
        return await self.redis_client.exists(self._get_profile_key(profile_id)) > 0
    
    async def get_profiles_count(self) -> int:
        try:
            return await self.redis_client.scard(self._get_profiles_key())
        except Exception as e:
            self.logger.error(f"Error getting profiles count: {e}")
            return 0
    
    async def clear_all_profiles(self) -> bool:
        try:
            keys = await self.redis_client.keys("profile:*")
            keys.append(self._get_profiles_key())
            
            if keys:
                await self.redis_client.delete(*keys)
            
            return True
        except Exception as e:
            self.logger.error(f"Error clearing profiles: {e}")
            return False
