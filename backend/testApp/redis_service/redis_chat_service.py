import redis.asyncio as redis
import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, Set, Optional, List
import os 

class RedisChatManager:
    def __init__(self, redis_url: str):
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        redis_db = int(os.getenv('REDIS_DB', 0))
        self.redis = redis.Redis(
                host=redis_host,
                port=redis_port,
                db=redis_db,
                decode_responses=True,
                socket_connect_timeout=5,
                retry_on_timeout=True
            )
        self.pubsub = self.redis.pubsub()

        self.channel_subscribers: Dict[str, Set[str]] = {}
        self.connection_channels: Dict[str, Set[str]] = {}
        self.connections: Dict[str, any] = {}

    async def connect(self):
        asyncio.create_task(self.start_listening())

    def generate_private_room_id(self, user1_id: str, user2_id: str) -> str:
        sorted_ids = sorted([user1_id, user2_id])
        return f"private:{sorted_ids[0]}:{sorted_ids[1]}"

    async def get_or_create_private_room(self, from_user_id: str, to_user_id: str, to_user_name: str) -> str:
        room_id = self.generate_private_room_id(from_user_id, to_user_id)
        exists = await self.redis.exists(f"chat:room:{room_id}")
        if not exists:
            await self._create_room(room_id, to_user_name, True, [from_user_id, to_user_id])
        return room_id

    async def create_group_room(self, name: str, creator_id: str, participant_ids: List[str]) -> str:
        room_id = f"group:{str(uuid.uuid4())}"
        all_participants = list(set([creator_id] + participant_ids))
        await self._create_room(room_id, name, False, all_participants)
        return room_id

    async def _create_room(self, room_id: str, name: str, is_private: bool, members: List[str]):
        now = datetime.utcnow().isoformat()
        await self.redis.hset(f"chat:room:{room_id}", mapping={
            "name": name,
            "is_private": str(is_private),
            "created_at": now,
            "creator_id": members[0] if members else ""
        })
        await self.redis.sadd(f"chat:room:{room_id}:members", *members)
        for user_id in members:
            await self.redis.sadd(f"user:{user_id}:rooms", room_id)
        print(f"Комната создана: {room_id}")

    async def send_message(self, from_user_id: str, room_id: str, text: str) -> str:
        is_member = await self.redis.sismember(f"chat:room:{room_id}:members", from_user_id)
        if not is_member:
            raise PermissionError("User not in room")

        message_data = {
            "from_user_id": from_user_id,
            "text": text,
            "timestamp": datetime.utcnow().isoformat()
        }
        message_id = await self.redis.xadd(
            f"chat:room:{room_id}:messages",
            message_data,
            maxlen=10000,
            approximate=True
        )

        await self.redis.set(f"user:{from_user_id}:last_seen:{room_id}", message_id)

        payload = {
            "type": "message",
            "room_id": room_id,
            "message_id": message_id,
            "from_user_id": from_user_id,
            "text": text,
            "timestamp": message_data["timestamp"]
        }
        await self.redis.publish(f"chat:room:{room_id}:events", json.dumps(payload))

        return message_id

    async def get_user_rooms(self, user_id: str) -> List[dict]:
        room_ids = await self.redis.smembers(f"user:{user_id}:rooms")
        rooms = []

        for room_id in room_ids:
            meta = await self.redis.hgetall(f"chat:room:{room_id}")
            if not meta:
                continue

            # Последнее сообщение
            last_msg = await self.redis.xrevrange(f"chat:room:{room_id}:messages", count=1)
            if last_msg:
                msg_data = last_msg[0][1]
                meta["last_message"] = msg_data.get("text", "")
                meta["last_message_time"] = msg_data.get("timestamp", "")

            # Непрочитанные
            last_seen_id = await self.redis.get(f"user:{user_id}:last_seen:{room_id}")
            if last_seen_id:
                unread_msgs = await self.redis.xrange(f"chat:room:{room_id}:messages", min=f"({last_seen_id}")
                meta["unread_count"] = len(unread_msgs)
            else:
                total = await self.redis.xlen(f"chat:room:{room_id}:messages")
                meta["unread_count"] = total

            # Для личных чатов — определяем собеседника
            if meta.get("is_private", "False").lower() == "true":
                # Извлекаем из room_id
                parts = room_id.split(":")
                if len(parts) >= 3:
                    user1, user2 = parts[1], parts[2]
                    other = user1 if user2 == user_id else user2
                    meta["other_user_id"] = other

            meta["room_id"] = room_id
            rooms.append(meta)

        # Сортировка по времени последнего сообщения
        rooms.sort(
            key=lambda x: x.get("last_message_time", "1970-01-01T00:00:00"),
            reverse=True
        )
        return rooms


    async def subscribe_connection_to_channel(self, connection_id: str, channel_name: str, websocket=None):
        if channel_name not in self.channel_subscribers:
            self.channel_subscribers[channel_name] = set()
            await self.pubsub.subscribe(channel_name)
            print(f"Redis начал слушать: {channel_name}")

        self.channel_subscribers[channel_name].add(connection_id)
        if connection_id not in self.connection_channels:
            self.connection_channels[connection_id] = set()
        self.connection_channels[connection_id].add(channel_name)
        if websocket:
            self.connections[connection_id] = websocket

    async def unsubscribe_connection_from_channel(self, connection_id: str, channel_name: str):
        if channel_name in self.channel_subscribers:
            self.channel_subscribers[channel_name].discard(connection_id)
            if len(self.channel_subscribers[channel_name]) == 0:
                await self.pubsub.unsubscribe(channel_name)
                del self.channel_subscribers[channel_name]

        if connection_id in self.connection_channels:
            self.connection_channels[connection_id].discard(channel_name)
            if len(self.connection_channels[connection_id]) == 0:
                self.connection_channels.pop(connection_id, None)
                self.connections.pop(connection_id, None)

    async def start_listening(self):
        print("Redis Pub/Sub слушатель запущен...")
        try:
            async for message in self.pubsub.listen():
                if message['type'] == 'message':
                    channel = message['channel']
                    data = message['data']
                    await self._route_message_to_subscribers(channel, data)
        except Exception as e:
            print(f"Ошибка в Redis слушателе: {e}")

    async def _route_message_to_subscribers(self, channel: str, message: str):
        if channel not in self.channel_subscribers:
            return

        for conn_id in list(self.channel_subscribers[channel]):
            ws = self.connections.get(conn_id)
            if ws and not ws.closed:
                try:
                    await ws.send_text(message)
                except Exception as e:
                    print(f"Ошибка отправки WebSocket {conn_id}: {e}")
                    await self.unsubscribe_connection_from_channel(conn_id, channel)


    async def set_user_online_in_room(self, user_id: str, room_id: str):
        await self.redis.sadd(f"chat:room:{room_id}:presence", user_id)
        await self.redis.setex(f"user:{user_id}:online_in:{room_id}", 30, "1")

    async def set_user_offline_in_room(self, user_id: str, room_id: str):
        await self.redis.srem(f"chat:room:{room_id}:presence", user_id)
        await self.redis.delete(f"user:{user_id}:online_in:{room_id}")

    async def get_room_online_users(self, room_id: str) -> List[str]:
        return list(await self.redis.smembers(f"chat:room:{room_id}:presence"))