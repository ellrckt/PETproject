from typing import Annotated, Dict
from fastapi import Cookie, Body, Depends, HTTPException, WebSocket, APIRouter, Request, WebSocketDisconnect
from redis_service.redis_profile_service import RedisJSONProfileService
from redis_service.redis_chat_service import RedisChatManager
from auth.utils import decode_jwt
from chats.chat_service import WebSocketManager
from testapp.dependencies import get_ws_service, profile_service, redis_json_service, get_redis_chat_service
from services.profile import ProfileService
from db.db import db_helper
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix='/chats',tags=['ws'])


@router.get("/get_user_rooms")
async def get_user_rooms(
    request: Request,
    ws_service: Annotated[WebSocketManager, Depends(get_ws_service)],
    profile_service: Annotated[ProfileService, Depends(profile_service)],
    redis_service: Annotated[RedisJSONProfileService, Depends(redis_json_service)],
    redis_chat_service: Annotated[RedisChatManager, Depends(get_redis_chat_service)],
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
        
    try:
        payload = decode_jwt(refresh_token)
        user_id = payload["user_id"]
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    receiver_ids = await redis_chat_service.get_user_receivers(user_id)
    if not receiver_ids:
        return {"data": None}
        
    user_rooms = await ws_service.get_user_rooms(user_id, receiver_ids)
    
    receivers_profiles = await profile_service.get_user_profiles(
        receiver_ids, redis_service, session
    )
    profiles_by_id = {p["user_id"]: p for p in receivers_profiles}
    
    rooms_with_profiles = []
    for room_id, room_data in user_rooms.items():
        receiver_id = room_data["receiver_id"]
        profile = profiles_by_id.get(receiver_id)
        
        if profile: 
            rooms_with_profiles.append({
                **room_data,
                "username": profile["username"],
                "profile_photo_url": profile["profile_photo_url"],
                "profile_id": profile["id"],
            })
            
    return {"data": rooms_with_profiles}
        
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

    # except KeyError:
    #     return {f"{user_id}": []}



@router.websocket("/ws/{receiver_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    receiver_id: int, 
    ws_service: Annotated[WebSocketManager, Depends(get_ws_service)],
):
    cookies_header = websocket.headers.get("cookie", "")
    refresh_token = None
    for cookie in cookies_header.split(";"):
        cookie = cookie.strip()
        if cookie.startswith("refresh_token="):
            refresh_token = cookie.split("=", 1)[1]
            break
    payload = decode_jwt(refresh_token)
    receiver_id = int(receiver_id)
    sender_id = int(payload["user_id"])
    room_id = ws_service._create_room_id(sender_id, receiver_id,)
    sender_username = payload["sub"]
    history = await ws_service.connect_room(websocket, sender_id, receiver_id, sender_username)
    
    try:
        # await websocket.accept()
        while True:
            data = await websocket.receive_text()
            await ws_service.broadcast(data, room_id, sender_id, receiver_id, sender_username)
    except WebSocketDisconnect:
        ws_service._disconnect(room_id, sender_id)

@router.post("/translate_message")
async def translate_message(
    ws_service: Annotated[WebSocketManager, Depends(get_ws_service)],
    message_id: str = Body(...),
    message_to_translate: str = Body(...),
    )->Dict:
    result = await ws_service.translate_message(message_to_translate)
    result["message_id"] = message_id
    print(result)
    return result

@router.post("/get_context_answer")
async def get_context_answer(
    request: Request,
    ws_service: Annotated[WebSocketManager, Depends(get_ws_service)],
    receiver_id: int = Body(...),
    )->Dict:
    user_id= decode_jwt(request.cookies.get("refresh_token"))["user_id"]
    result = await ws_service.get_context_answer(user_id, receiver_id)
    return result

    # @router.get("/get_context_answer")
    # async def get_context_answer(
    #     ws_service: Annotated[WebSocketManager, Depends(get_ws_service)],
    #     request: Request,
    #     )->Dict:
    #     refresh_token = request.cookies.get("refresh_token")
    #     sender_id = decode_jwt(refresh_token)["user_id"]
    #     ws_service.get_context_answer()
        