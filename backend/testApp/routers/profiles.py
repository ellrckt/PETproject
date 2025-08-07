from testapp.dependencies import user_service, user_crud_service
from schemas.user.user import UserCreation, UserResponse, UserUpdate,UserEmailConffirmation,UserLocation,UserCityCountry
from services.user import UserService
from typing import Annotated, List
from fastapi import Depends, APIRouter, Request, Response
from fastapi.security import HTTPBearer
from db.db import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from routers.login import check_jwt
from auth.utils import decode_jwt, encode_jwt
from fastapi import Request

router = APIRouter(tags=["profiles"], prefix="/profile")


@router.get("/get_user_location")
async def get_user_location(
    session: Annotated[AsyncSession,Depends(db_helper.get_session)],
    user_service: Annotated[UserService,Depends(user_service)],
    schema: UserLocation,
    request: Request,
    )->UserCityCountry:

    result = await user_service.get_user_location(schema,session,request)
    return UserCityCountry(city = result.city, country = result.country)