from fastapi import APIRouter, Depends
from schemas.user.user import UserRegistration
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import db_helper
from services.user import UserService
from testapp.dependencies import user_service
from schemas.user.user import UserResponse
from typing import Annotated

router = APIRouter(tags=["registration"], prefix="/registration")


@router.post("", response_model=UserResponse)
async def register_user(
    schema: UserRegistration,
    user_service: Annotated[UserService, Depends(user_service)],
    session: AsyncSession = Depends(db_helper.get_session),
) -> UserResponse:

    result = await user_service.register_user(schema, session)
    return result
