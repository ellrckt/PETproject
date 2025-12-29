from http.client import HTTPResponse
from typing import Mapping

from fastapi import HTTPException
import redis.asyncio as redis
import json
import os
from typing import Optional


class RedisChatManager:
    def __init__(self):
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        redis_db = int(os.getenv("REDIS_DB", 0))
        self.redis = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            decode_responses=True,
            socket_connect_timeout=5,
        )

    async def _create_room_id(self, room_id: str, sender_id: int, receiver_id: int):
        try:
            with self.redis.pipeline(transaction=True) as pipe:
                pipe.lpush(room_id, sender_id)
                pipe.rpush(room_id, receiver_id)
                pipe.execute()
                
                return True
        
        except redis.RedisError as e:
            return False
        except Exception as e:
            return e

    def _create_room_history_prefix(self, room_prefix: str):
        prefix = f"{room_prefix}:history"
        return prefix
    
    def _create_unread_messages_prefix(self, room_id: str, receiver_id: int):
        prefix = f"{room_id}:{receiver_id}:unread_messages"
        return prefix
    
    async def add_unread_message(self,room_id: str, receiver_id: int):

        prefix = self._create_unread_messages_prefix(room_id, receiver_id)
        try: 
            await self.redis.incr(prefix)
            await self.redis.expire(prefix, 60*60*24*30)
        except Exception as e:
            print(f"Redis error in add_unread_message: {e}")
            return False

    async def add_history_message(self, room_id: str, message_data: dict):
        history_key = self._create_room_history_prefix(room_id)
        
        try:
            message_json = json.dumps(message_data, ensure_ascii=False)
            ### Pipeline
            await self.redis.rpush(history_key, message_json)
            await self.redis.ltrim(history_key, 0, 999)  
            await self.redis.expire(history_key, 60 * 60 * 24 * 10)  
            
            return True
            
        except Exception as e:
            return HTTPException(status_code=500, detail="Adding message to the history error")
    
    
    async def get_unread_messages(self,room_id: str, sender_id: int):

        prefix = self._create_unread_messages_prefix(room_id, sender_id)
        try:
            value = await self.redis.get(prefix)

            if value:
                count = int(value)
            else:
                count = 0  
            await self.redis.set(prefix, 0)    
            return count
        
            
        except Exception as e:
            raise HTTPException(status_code=500, detail="Unread data receiving error")
        
    

    async def get_recent_messages(self, room_id: str, limit: int = 50):

        history_key = self._create_room_history_prefix(room_id)
        
        try:
            messages_json = await self.redis.lrange(history_key, 0, limit - 1)
            
            messages = []
            for msg_json in messages_json:
                try:
                    messages.append(json.loads(msg_json))
                except json.JSONDecodeError:
                    return HTTPException(status_code=500, detail='History messages serialization error')
            
            return messages
            
        except Exception as e:
            return HTTPException(status_code=500, detail="History data receiving error")
    
    async def get_last_n_messages(self, room_id: str, n: int = 3):

        history_key = self._create_room_history_prefix(room_id)
        print(history_key)
        try:
            messages_json = await self.redis.lrange(history_key, -n, -1)
            messages = []
            for msg_json in messages_json:
                try:
                    messages.append(json.loads(msg_json))
                except json.JSONDecodeError:
                    continue
            print("MESSAGES", messages)
            return messages
    

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_last_message(self, room_id: str):
        history_key = self._create_room_history_prefix(room_id)
        last_message = await self.redis.lindex(history_key, -1)
        if not last_message:
            return {'message': None}
        json_message = json.loads(last_message)
        return json_message
    
# async def test_redis():
#     a = RedisChatManager() 
#     await a.add_unread_message("42_36", 36)
#     await a.add_unread_message("42_36", 36)
#     await a.add_unread_message("42_36", 36)
    
#     count = await a.get_unread_messages("42_36", 36)
#     print(f"Unread messages count: {count}")

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(test_redis())