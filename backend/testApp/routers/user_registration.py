from fastapi import APIRouter, Depends, Response, Request
from schemas.user.user import UserRegistration
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import db_helper
from services.user import UserService
from testapp.dependencies import user_service
from schemas.user.user import UserResponse
from schemas.token.token import TokenInfo
from typing import Annotated
import random
import string
router = APIRouter(tags=["registration"], prefix="/registration")
from auth.utils import encode_jwt,REFRESH_TOKEN_TYPE,ACCESS_TOKEN_TYPE
from routers.profiles import update_profile
from schemas.profiles.profile import UpdateProfile


@router.post("", response_model=TokenInfo)
async def register_user(
    schema: UserRegistration,
    user_service: Annotated[UserService, Depends(user_service)],
    response: Response,
    request: Request,
    session: AsyncSession = Depends(db_helper.get_session),
) -> UserResponse:

    result = await user_service.register_user(schema, session)
    payload = {
                "sub": result.username,
                "email": result.email,
                "token_type": REFRESH_TOKEN_TYPE,
                }
    test_profile = UpdateProfile(
    username=result.username,
    age=None, 
    city=None,
    country=None,
    about_user=None,
    user_habits=None
)
    refresh_token = encode_jwt(payload)
    profile = await user_service.update_profile(session,refresh_token,test_profile)
    await session.commit()
    user_session = await user_service.create_user_session(result,refresh_token,session)
    payload = {
                "sub": result.username,
                "email": result.email,
                "token_type": ACCESS_TOKEN_TYPE,
                }
    
    access_token = encode_jwt(payload) 
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=3600,
        path="/",
    )
    return TokenInfo(refresh_token=refresh_token,access_token=access_token)
