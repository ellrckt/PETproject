from typing import Dict, Set, List
from datetime import datetime
from fastapi import WebSocket,WebSocketDisconnect,Depends
from typing import Annotated
from redis_service.redis_chat_service import RedisChatManager
from testapp.dependencies import get_redis_chat_service, get_translate_manager
from translate_manager.translate_manager import TranslatorManager
import uuid
import json
class WebSocketManager:

    active_connections: Dict[str, Dict[int, WebSocket]] = {}
    rooms: Dict[str, List[int]] ={}
    user_rooms: Dict[int, Set[str]] ={}
    redis_service: RedisChatManager = RedisChatManager()
    translate_manager: TranslatorManager = TranslatorManager()

    def generate_uuid_v4(self) -> str:
        return str(uuid.uuid4())
    
    def _create_room_id(self, sender_id: int, receiver_id: int) -> str:
        sorted_ids = sorted([sender_id, receiver_id])
        return f"{sorted_ids[0]}_{sorted_ids[1]}"

    async def _connect(
        self, websocket: WebSocket, sender_id: int, receiver_id: int, room_id: str
    ):

        await websocket.accept()

        if room_id not in self.active_connections:
            self.active_connections[room_id] = {}
        self.active_connections[room_id][sender_id] = websocket

    async def _create_room(
        self, websocket: WebSocket, sender_id: int, receiver_id: int
    ):
        room_id = self._create_room_id(sender_id, receiver_id)
        
        if sender_id not in self.user_rooms:
            self.user_rooms[sender_id] = set()
            
        if receiver_id not in self.user_rooms:
            self.user_rooms[receiver_id] = set()
        
        if room_id not in self.rooms:
            self.rooms[room_id] = []    
        
        self.rooms[room_id].append(sender_id)
        self.rooms[room_id].append(sender_id)
        self.user_rooms[sender_id].add(room_id)   
        self.user_rooms[receiver_id].add(room_id)
        await self._connect(websocket, sender_id, receiver_id, room_id)

    async def connect_room(
        self, websocket: WebSocket, sender_id: int, receiver_id: int, sender_username: str
    ):
        sender_id = int(sender_id)
        history_limit = 50
        room_id = self._create_room_id(sender_id, receiver_id)
        history_messages = await self.redis_service.get_recent_messages(room_id, history_limit)
        print("History",history_messages)
        for message in history_messages:
            message["is_viewed"] = True
        unread_messages_count = await self.redis_service.get_unread_messages(room_id, sender_id)
        if room_id not in self.user_rooms:
            await self._create_room(websocket, sender_id, receiver_id)
        else:
            await self._connect(websocket, sender_id, receiver_id)
        for message in history_messages:
            try:
                await websocket.send_text(json.dumps({
                    "type": "history",
                    "data": message
                }))
            except Exception as e:
                print(f"Error sending history: {e}")
        # return {"history": history_messages, "sender_unread_messages_count": unread_messages_count}
    
    async def delete_room(self, room_id: int, sender_id: int, receiver_id: int):

        self.rooms[room_id].remove(sender_id)
        self.user_rooms[sender_id].remove(room_id)
        await self._disconnect(room_id, sender_id)

        self.rooms[room_id].remove(receiver_id)
        self.user_rooms[receiver_id].remove(room_id)
        await self._disconnect(room_id, receiver_id)

    def _disconnect(self, room_id: int, user_id: int):

        if (
            room_id in self.active_connections
            and user_id in self.active_connections[room_id]
        ):
            del self.active_connections[room_id][user_id]
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]


    async def broadcast(self, message: str, room_id: int, sender_id: int, receiver_id: int, sender_username: str):
        
        if room_id in self.active_connections:
            message_with_class = {"message": message, "sender_id": sender_id, "receiver_id": receiver_id, "date": datetime.now().isoformat(), "is_viewed": True, "message_id": self.generate_uuid_v4(), "username": sender_username}
            
            if receiver_id not in self.active_connections[room_id]:
                message_with_class["is_viewed"] = False
                await self.redis_service.add_unread_message(room_id, receiver_id)
                history = await self.redis_service.add_history_message(room_id, message_with_class)
            else:
                 await self.redis_service.add_history_message(room_id, message_with_class)
                
            for user_id, connection in self.active_connections[room_id].items():
                await connection.send_json(message_with_class)

    async def get_user_rooms(self, user_id: int):
        try:
            user_rooms = self.user_rooms[user_id] 
            user_rooms_to_represent = {}
            for room_id in user_rooms:
                receiver_id = self.rooms[room_id][0]
                if receiver_id == user_id:
                    receiver_id = self.rooms[room_id][1]
                last_message = await self.redis_service.get_last_message(room_id)
                user_rooms_to_represent[room_id] = {"sender_id": user_id,"room_id": room_id, "last_message": last_message, "receiver_id": receiver_id}
            return user_rooms_to_represent
        except KeyError:
            raise KeyError
            
    async def get_context_answer(self, messages: Dict, room_id: str, receiver_id: int)->Dict:

        unread_messages_count = await self.redis_service.add_unread_message(room_id, receiver_id)
        unread_messages = await self.redis_service.get_last_n_messages(room_id, unread_messages_count)
        context_answer = self.translate_manager.context_answer(unread_messages)

        return {"answer": context_answer}
    
    def translate_message(self, message: str):
        translation = self.translate_manager.translate(message)
        return {"translation": translation}
        # async def _get_room_history(self, room_id: str):
    #     history_messages =  await self.redis_service.get_recent_messages(room_id)
    #     return history_messages

       
