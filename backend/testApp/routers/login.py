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


def check_jwt(request: Request):
    token = request.cookies.get("access_token")
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
    response.set_cookie(
        key="access_token", value=result, httponly=True, secure=True, samesite="Lax"
    )
    return TokenInfo(
        access_token=result,
        token_type="Bearer",
    )
