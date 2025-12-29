from typing import Annotated, Dict
from fastapi import Cookie, Body, Depends, WebSocket, APIRouter, Request, WebSocketDisconnect
from idna import decode
from redis_service.redis_profile_service import RedisJSONProfileService
from auth.utils import decode_jwt
from chats.chat_service import WebSocketManager
from testapp.dependencies import get_ws_service, profile_service, redis_json_service
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
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
):
    refresh_token = request.cookies.get("refresh_token")
    user_id = decode_jwt(refresh_token)["user_id"]
    try:
        user_rooms = await ws_service.get_user_rooms(user_id) 
        #{"room_id": {"sender_id": user_id,"room_id": room_id,
        #last_message": last_message, "receiver_id": receiver_id}}
        # {'4_6': {'sender_id': 6, 'room_id': '4_6', 'last_message': {'message': None}, 'receiver_id': 4}}
        receiver_ids = [room["receiver_id"] for room in user_rooms.values()]

        receivers_profiles = await profile_service.get_user_profiles(receiver_ids, redis_service, session)
        print(receivers_profiles)
        profiles_by_id = {profile["user_id"]: profile for profile in receivers_profiles}

        rooms_with_profiles = {
            room_id: {
                **room_data,  
                "username": profiles_by_id[room_data["receiver_id"]]["username"],
                "profile_photo_url": profiles_by_id[room_data["receiver_id"]]["profile_photo_url"],
                "profile_id": profiles_by_id[room_data["receiver_id"]]["id"],
            }
            for room_id, room_data in user_rooms.items()  
            if room_data["receiver_id"] in profiles_by_id
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
        