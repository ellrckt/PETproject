from fastapi import APIRouter, Depends, Response
from schemas.user.user import UserRegistration
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import db_helper
from services.user import UserService
from testapp.dependencies import user_service
from schemas.user.user import UserResponse
from typing import Annotated
import random
import string
router = APIRouter(tags=["registration"], prefix="/registration")
from auth.utils import encode_jwt,REFRESH_TOKEN_TYPE

@router.post("", response_model=UserResponse)
async def register_user(
    schema: UserRegistration,
    user_service: Annotated[UserService, Depends(user_service)],
    response: Response,
    session: AsyncSession = Depends(db_helper.get_session),
) -> UserResponse:

    result = await user_service.register_user(schema, session)
    payload = {
                "sub": result.username,
                "email": result.email,
                "token_type": REFRESH_TOKEN_TYPE,
                }
    refresh_token = encode_jwt(payload)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=3600,
        path="/",
    )
    return result
