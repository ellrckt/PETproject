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
    user_rooms = await ws_service.get_user_rooms(user_id)
    receiver_ids = [room["receiver_id"] for room in user_rooms]
    receivers_profiles = await profile_service.get_user_profiles(receiver_ids, redis_service)
    print(f"PROFILES: {receivers_profiles}")
    return user_rooms



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
