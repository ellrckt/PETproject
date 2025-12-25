from typing import Annotated
from fastapi import Depends, WebSocket, APIRouter, Request, WebSocketDisconnect
from redis_service.redis_profile_service import RedisJSONProfileService
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import db_helper
from auth.utils import decode_jwt
from chats.chat_service import WebSocketManager
from redis_service.redis_chat_service import RedisChatManager
from routers.auth import refresh_token
from testapp.dependencies import get_ws_service, profile_service, redis_json_service
from services.profile import ProfileService

router = APIRouter(prefix='/ws/chats',tags=['ws'])

@router.get("/get_user_rooms")
async def get_user_rooms(
    request: Request,
    ws_service: Annotated[WebSocketManager, Depends(get_ws_service)],
    profile_service: Annotated[ProfileService, Depends(profile_service)],
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    redis_service: Annotated[RedisJSONProfileService, Depends(redis_json_service)]
):
    refresh_token = request.cookies.get("refresh_token")
    user_id = decode_jwt(refresh_token)["user_id"]
    try:
        user_rooms = await ws_service.get_user_rooms(user_id) 
        #{"room_id": {"sender_id": user_id,"room_id": room_id,
        #last_message": last_message, "receiver_id": receiver_id}}

        receiver_ids = [room["receiver_id"] for room in user_rooms]
        receivers_profiles = await profile_service.get_user_profiles(receiver_ids, redis_service)
        profiles_by_id = {profile["user_id"]: profile for profile in receivers_profiles}

        rooms_with_profiles = {
            room["room_id"]: {
                **room,  
                "username": profiles_by_id[room["receiver_id"]]["username"],
                "profile_photo_url": profiles_by_id[room["receiver_id"]]["profile_photo_url"],
                "profile_id": profiles_by_id[room["receiver_id"]]["id"],
            }
            for room in user_rooms 
            if room["receiver_id"] in profiles_by_id
            }
        return rooms_with_profiles
        
        #user_rooms_to_represent 
        #[{
        #    "user_id": 0,
        #    "username": "string",
        #    "age": 0,
        #    "city": "string",
        #    "country": "string",
        #    "about_user": "string",
        #    "user_habits": [
        #        "string"
        #    ],
        #    "profile_photo_url": "string"
        #    },]

    except KeyError:
        return {f"{user_id}": []}



@router.websocket("/{receiver_id}")
async def websocket_endpoint(
    request: Request,
    websocket: WebSocket, 
    receiver_id: int, 
    ws_service: Annotated[WebSocketManager, Depends(get_ws_service)],
):
    sender_id = decode_jwt(request.cookies.get("refresh_token"))["user_id"]
    room_id = ws_service._create_room_id(sender_id, receiver_id,)
    await ws_service.connect(websocket, room_id, sender_id)

    try:
        while True:
            data = await websocket.receive_text()
            await ws_service.broadcast(data, room_id, sender_id, receiver_id)
    except WebSocketDisconnect:
        ws_service.disconnect(room_id, sender_id)
