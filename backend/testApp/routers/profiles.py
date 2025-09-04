from testapp.dependencies import profile_service
from schemas.profiles.profile import Profile
from services.profile import ProfileService
from typing import Annotated
from fastapi import Depends, APIRouter, Request, UploadFile
from db.db import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from schemas.profiles.profile import UpdateProfile
from services.auth import AuthService
from testapp.dependencies import auth_service, redis_json_service
from redis_service.redis_profile_service import RedisJSONProfileService
FOLDER = "profiles_photo"

router = APIRouter(tags=["profiles"], prefix="/profile")


@router.get("/get_user_profile")
async def get_user_profile(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    profile_service: Annotated[ProfileService, Depends(profile_service)],
    redis_service: Annotated[RedisJSONProfileService, Depends(redis_json_service)],
) -> Profile:
    refresh_token = request.cookies.get("refresh_token")
    result = await profile_service.get_user_profile(session,redis_service, refresh_token)
    

    return result


@router.patch("/update_profile")
async def update_profile(
    request: Request,
    schema: UpdateProfile,
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    profile_service: Annotated[ProfileService, Depends(profile_service)],
    redis_service: Annotated[RedisJSONProfileService, Depends(redis_json_service)],
) -> Profile:
    refresh_token = request.cookies.get("refresh_token")
    result = await profile_service.update_profile(session, refresh_token, schema, redis_service)

    return result


@router.post("/create_profile")
async def create_profile(
    request: Request,
    schema: UpdateProfile,
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    profile_service: Annotated[ProfileService, Depends(profile_service)],
) -> Profile:
    refresh_token = request.cookies.get("refresh_token")
    result = await profile_service.create_profile(session, refresh_token, schema)

    return result


@router.post("/upload_user_profile_photo")
async def upload_user_profile_photo(
    request: Request,
    file: UploadFile,
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    auth_service: Annotated[AuthService,Depends(auth_service)],
    profile_service: Annotated[ProfileService, Depends(profile_service)],
):
    refresh_token = request.cookies.get("refresh_token")
    result = await profile_service.upload_user_profile_photo(auth_service, refresh_token, session, file, FOLDER)

    return result
