from testapp.dependencies import user_service, user_crud_service
from schemas.profiles.profile import Profile
from services.user import UserService
from schemas.user.user import UserCityCountry,UserLocation
from typing import Annotated, List
from fastapi import Depends, APIRouter, Request, Response
from db.db import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request,Response
from schemas.profiles.profile import Hobbies,UpdateProfile

router = APIRouter(tags=["profiles"], prefix="/profile")


@router.post("/get_user_location")
async def get_user_location(
    session: Annotated[AsyncSession,Depends(db_helper.get_session)],
    user_service: Annotated[UserService,Depends(user_service)],
    schema: UserLocation,
    request: Request,
    )->UserCityCountry:

    result = await user_service.get_user_location(schema,session,request)
    return UserCityCountry(city = result.city, country = result.country)

@router.get("/get_hobbies")
async def get_hobbies(
    session: Annotated[AsyncSession,Depends(db_helper.get_session)],
    user_service: Annotated[UserService,Depends(user_service)]
    )->List[str]:
    result = await user_service.get_hobbies(session)
    return result

@router.get("/get_user_profile")
async def get_user_profile(
    request: Request,
    session: Annotated[AsyncSession,Depends(db_helper.get_session)],
    user_service: Annotated[UserService,Depends(user_service)]
)->Profile:  
    refresh_token = request.cookies.get("refresh_token")
    result = await user_service.get_user_profile(session,refresh_token)
    return result
    
@router.patch("/update_profile")
async def update_profile(
    request: Request,
    schema: UpdateProfile,
    session: Annotated[AsyncSession,Depends(db_helper.get_session)],
    user_service: Annotated[UserService,Depends(user_service)],
)->Profile:  
    refresh_token = request.cookies.get("refresh_token")
    result = await user_service.update_profile(session,refresh_token,schema)
    return result

@router.post("/create_profile")
async def create_profile(
    request: Request,
    schema: UpdateProfile,
    session: Annotated[AsyncSession,Depends(db_helper.get_session)],
    user_service: Annotated[UserService,Depends(user_service)],
)->Profile:  
    refresh_token = request.cookies.get("refresh_token")
    result = await user_service.create_profile(session,refresh_token,schema)
    return result