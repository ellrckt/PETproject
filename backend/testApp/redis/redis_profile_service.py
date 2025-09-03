import redis
from redis.commands.json.path import Path
import os
from typing import Optional, Dict, Any, List
import logging

class RedisJSONProfileService:
    def __init__(self):
        self.logger = logging.getLogger("redis_service")
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        redis_password = os.getenv('REDIS_PASSWORD', None)
        redis_db = int(os.getenv('REDIS_DB', 0))

        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            password=redis_password,
            decode_responses=True,
            socket_connect_timeout=5,
            retry_on_timeout=True
        )
        
        self.json_client = self.redis_client.json()
        
        try:
            self.redis_client.ping()
            self.logger.debug("Redis is OK")
        except redis.ConnectionError:
            self.logger.debug("Failed to connect to Redis JSON")
            
    def _get_profile_key(self, profile_id: str) -> str:
        self.logger.debug("Generating profile key")
        return f"profile:{profile_id}"
    
    def _get_profiles_key(self) -> str:
        self.logger.debug("Generating profiles key")
        return "profiles:all"
    
    def create_profile(self, profile_id: str, profile_data: Dict[str, Any], 
                      expire_seconds: Optional[int] = None) -> bool:
        self.logger.debug("Creating Redis profile")
        try:
            key = self._get_profile_key(profile_id)
            self.json_client.set(key, Path.root_path(), profile_data)            
            self.redis_client.sadd(self._get_profiles_key(), profile_id)
            return True
        except Exception as e:
            self.logger.error(f"Error creating profile: {e}")
            return False
    
    def get_profile(self, profile_id: str) -> Optional[Dict[str, Any]]:

        try:
            key = self._get_profile_key(profile_id)
            return self.json_client.get(key)
        except Exception as e:
            self.logger.error(f"Error getting profile: {e}")
            return None
    
    def get_profile_field(self, profile_id: str, field: str) -> Any:
        
        try:
            key = self._get_profile_key(profile_id)
            result = self.json_client.get(key, f".{field}")
            return result
        except Exception as e:
            self.logger.error(f"Error getting field {field}: {e}")
            return None
    
    def update_profile(self, profile_id: str, updates: Dict[str, Any]) -> bool:
       
        try:
            key = self._get_profile_key(profile_id)
            
            for field, value in updates.items():
                self.json_client.set(key, f".{field}", value)
            
            return True
        except Exception as e:
            self.logger.error(f"Error updating profile: {e}")
            return False
    
    def delete_profile(self, profile_id: str) -> bool:

        try:
            key = self._get_profile_key(profile_id)
            result = self.redis_client.delete(key)
            self.redis_client.srem(self._get_profiles_key(), profile_id)
            
            return result > 0
        except Exception as e:
            self.logger.error(f"Error deleting profile: {e}")
            return False
    
    def get_all_profiles(self) -> List[Dict[str, Any]]:

        try:
            profile_ids = self.redis_client.smembers(self._get_profiles_key())
            
            profiles = []
            for profile_id in profile_ids:
                profile = self.get_profile(profile_id)
                if profile:
                    profiles.append({
                        'id': profile_id,
                        **profile
                    })
            
            return profiles
        except Exception as e:
            self.logger.error(f"Error getting all profiles: {e}")
            return []
    
    def search_profiles(self, field: str, value: Any) -> List[Dict[str, Any]]:

        try:
            all_profiles = self.get_all_profiles()
            return [profile for profile in all_profiles 
                   if profile.get(field) == value]
        except Exception as e:
            self.logger.error(f"Error searching profiles: {e}")
            return []
    
    def search_profiles_jsonpath(self, jsonpath_query: str) -> List[Dict[str, Any]]:
 
        try:
            results = []
            profile_ids = self.redis_client.smembers(self._get_profiles_key())
            
            for profile_id in profile_ids:
                key = self._get_profile_key(profile_id)
                try:
                    result = self.json_client.get(key, jsonpath_query)
                    if result and result != []: 
                        results.append({
                            'id': profile_id,
                            'data': result
                        })
                except:
                    continue
            
            return results
        except Exception as e:
            print(f"Error searching with JSONPath: {e}")
            return []
    
    def profile_exists(self, profile_id: str) -> bool:

        return self.redis_client.exists(self._get_profile_key(profile_id)) > 0
    
    def get_profiles_count(self) -> int:

        try:
            return self.redis_client.scard(self._get_profiles_key())
        except Exception as e:
            print(f"Error getting profiles count: {e}")
            return 0
    
    def clear_all_profiles(self) -> bool:

        try:
            keys = self.redis_client.keys("profile:*")
            keys.append(self._get_profiles_key())
            
            if keys:
                self.redis_client.delete(*keys)
            
            return True
        except Exception as e:
            print(f"Error clearing profiles: {e}")
            return False

redis_json_service = RedisJSONProfileService()


# if __name__ == "__main__":
#     service = RedisJSONProfileService()
    
#     profile_data = {
#         "name": "John Doe",
#         "age": 25,
#         "email": "john@example.com",
#         "interests": ["sports", "music", "travel"],
#         "address": {
#             "city": "New York",
#             "zipcode": "10001",
#             "coordinates": {
#                 "lat": 40.7128,
#                 "lng": -74.0060
#             }
#         },
#         "premium": True,
#         "settings": {
#             "notifications": True,
#             "language": "en"
#         }
#     }
    
#     service.create_profile("user_123", profile_data)
    
#     profile = service.get_profile("user_123")
#     print("Full profile:", profile)
    
#     city = service.get_profile_field("user_123", "address.city")
#     print("City:", city)
    
#     service.update_profile("user_123", {
#         "age": 26,
#         "address.city": "Brooklyn",
#         "interests": ["sports", "music", "travel", "food"]
#     })
    
#     results = service.search_profiles_jsonpath("$[?(@.age > 25)]")
#     print("Profiles older than 25:", results)
    
#     all_profiles = service.get_all_profiles()
#     print("All profiles:", all_profiles)
    
#     count = service.get_profiles_count()
#     print("Total profiles:", count)