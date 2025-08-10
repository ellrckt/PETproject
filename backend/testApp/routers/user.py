from testapp.dependencies import user_service, user_crud_service
from schemas.user.user import UserCreation, UserResponse, UserUpdate,UserLocation,UserCityCountry
from services.user import UserService
from typing import Annotated, List
from fastapi import Depends, APIRouter, Request, Response
from fastapi.security import HTTPBearer
from db.db import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from routers.login import check_jwt
from auth.utils import decode_jwt, encode_jwt
from fastapi import Request
router = APIRouter(tags=["user_crud"], prefix="/user")

http_bearer = HTTPBearer()


@router.post("/user_create")
async def create_user(
    schema: UserCreation,
    user_service: Annotated[UserService, Depends(user_crud_service)],
    session: AsyncSession = Depends(db_helper.get_session),
) -> UserResponse:
    user_instance = await user_service.add_one(schema, session)
    return UserResponse(
        id=user_instance.id,
        username=user_instance.username,
        email=user_instance.email,
        password=user_instance.password,
    )

@router.get("/get_user_by_email")
async def get_user_by_email(
    user_service: Annotated[UserService,Depends(user_crud_service)],
    session: Annotated[AsyncSession,Depends(db_helper.get_session)],
    request: Request
):
    refresh_token = request.get_cookies("refresh_token")
    email = decode_jwt(refresh_token)["email"]
    print(email)
    result = await user_crud_service.get_user_by_email(session,email)
    

@router.get("/get_users")
async def get_all_users(
    user_service: Annotated[UserService, Depends(user_crud_service)],
    headers: str = Depends(http_bearer),
    session: AsyncSession = Depends(db_helper.get_session),
):
    access_token = headers.credentials
    payload = check_jwt(access_token)
    result = await user_service.get_all(session)
    return result


@router.delete("/delete/{user_id}", response_model=UserResponse)
async def delete_user(
    user_id: int,
    user_service: Annotated[UserService, Depends(user_crud_service)],
    session: AsyncSession = Depends(
        db_helper.get_session,
    ),
) -> UserResponse:
    result = await user_service.delete(user_id, session)
    return result


@router.patch("/update")
async def update_user(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    user_service: Annotated[UserService, Depends(user_crud_service)],
    request: Request,
    schema: UserUpdate,
) -> UserResponse:
    payload = decode_jwt(request.cookies.get("access_token"))
    result = await user_service.update(schema, session, payload)
    return result
