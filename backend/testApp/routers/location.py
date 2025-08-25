from typing import Annotated
from fastapi import Depends, APIRouter, Request
from sqlalchemy.ext.asyncio import AsyncSession

from testapp.dependencies import location_service,profile_service
from services.location import LocationService
from services.profile import ProfileService
from schemas.user.user import UserCityCountry, UserLocation
from db.db import db_helper
from schemas.profiles.profile import  UpdateProfile

router = APIRouter(tags=["location"], prefix="/user_location")

@router.post("/set_user_lat_lng")
async def set_user_lat_lng(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    location_service: Annotated[LocationService, Depends(location_service)],
    profile_service: Annotated[ProfileService, Depends(profile_service)],
    schema: UserLocation,
    request: Request,
) -> UserCityCountry:
    
    refresh_token = request.cookies.get("refresh_token")
    result = await location_service.set_user_lat_lng(schema, session, request)

    location = await profile_service.update_profile(
    session, 
    refresh_token, 
    UpdateProfile(city=result.city, country=result.country)
    )

    return UserCityCountry(city=result.city, country=result.country)
