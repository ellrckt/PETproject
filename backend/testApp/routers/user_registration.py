from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import db_helper
from schemas.token.token import TokenInfo
from schemas.user.user import UserRegistration
from services.user import UserService
from testapp.dependencies import user_service

router = APIRouter(tags=["registration"], prefix="/registration")

@router.post("", response_model=TokenInfo)
async def register_user(
    schema: UserRegistration,
    user_service: Annotated[UserService, Depends(user_service)],
    response: Response,
    session: AsyncSession = Depends(db_helper.get_session),
) -> TokenInfo:

    try:
        refresh_token, access_token = await user_service.register_user(schema, session)
        
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=3600 * 24 * 7,
            path="/",
        )
        
        return TokenInfo(refresh_token=refresh_token, access_token=access_token)
        
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")
