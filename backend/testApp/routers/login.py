from fastapi import APIRouter, Depends, Form, Response, Request
from schemas.user.user import UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import db_helper
from services.user import UserService
from testapp.dependencies import user_service
from schemas.user.user import UserResponse
from typing import Annotated
from schemas.token.token import TokenInfo
from config import settings
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException

router = APIRouter(tags=["login"], prefix="/login")


def check_jwt(access_token: str):
    token = access_token
    try:
        payload = jwt.decode(
            token,
            settings.auth_jwt.public_key_path.read_text(),
            algorithms=settings.auth_jwt.algorithm,
        )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("", response_model=TokenInfo)
async def login_user(
    schema: UserLogin,
    user_service: Annotated[UserService, Depends(user_service)],
    response: Response,
    session: AsyncSession = Depends(db_helper.get_session),
):
    result = await user_service.login_user(schema, session)
    refresh_token = result.refresh_token
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=3600,
        path="/",
    )

    # response.set_cookie(
    #     key="refresh_token",
    #     value=refresh_token,
    #     httponly=True,
    #     secure=False,  # Уберите это для локальной разработки без HTTPS
    #     samesite="Lax",
    #     max_age=3600,
    #     domain="localhost",  # Или ваш домен
    #     path="/",  # Или путь к вашему API
    # )

    return result


# @router.post("", response_model=TokenInfo)
# async def login_user(
#     schema: UserLogin,
#     user_service: Annotated[UserService, Depends(user_service)],
#     response: Response,
#     session: AsyncSession = Depends(db_helper.get_session),
# ):
#     result = await user_service.login_user(schema, session)

#     # response.set_cookie(
#     #     key="access_token",
#     #     value=result.access_token,
#     #     httponly=True,
#     #     secure=True,
#     #     samesite="Lax",
#     #     max_age=3600,
#     # )
#     response.set_cookie(
#         key="refresh_token",
#         value=result.refresh_token,
#         httponly=True,
#         secure=True,
#         samesite="Lax",
#         max_age=3600,
#     )

#     return result


@router.post("/refresh")
async def refresh_token(
    response: Response,
    request: Request,
    user_service: Annotated[UserService, Depends(user_service)],
    session: AsyncSession = Depends(db_helper.get_session),
) -> TokenInfo:
    refresh_token = request.cookies.get("refresh_token")
    access_token = request.cookies.get("access_token")
    new_access_token = await user_service.refresh_token(
        session, access_token, refresh_token
    )
    return TokenInfo(
        access_token=new_access_token,
        # refresh_token=request.cookies.get("refresh_token"),
    )
