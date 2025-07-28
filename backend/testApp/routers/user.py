# импорты TaskRepo и фастапи роутеров
from testapp.dependencies import user_service
from schemas.user.user import UserCreation, UserResponse,UserUpdate
from services.user import UserService
from typing import Annotated, List
from fastapi import Depends, APIRouter,Request,Response
from db.db import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from routers.login import check_jwt
from auth.utils import decode_jwt,encode_jwt

router = APIRouter(tags=["user_crud"], prefix="/user")


@router.post("/user_create")
async def create_user(
    schema: UserCreation,
    user_service: Annotated[UserService, Depends(user_service)],
    session: AsyncSession = Depends(db_helper.get_session),
) -> UserResponse:
    user_instance = await user_service.add_one(schema, session)
    return UserResponse(
        id=user_instance.id,
        username=user_instance.username,
        email=user_instance.email,
        password=user_instance.password,
    )


@router.get(
    "/get_users", response_model=List[UserResponse], dependencies=[Depends(check_jwt)]
)
async def get_all_users(
    user_service: Annotated[UserService, Depends(user_service)],
    session: AsyncSession = Depends(db_helper.get_session),
) -> dict[UserResponse]:
    result = await user_service.get_all(session)
    return result


@router.delete("/delete/{user_id}", response_model=UserResponse)
async def delete_user(
    user_id: int,
    user_service: Annotated[UserService, Depends(user_service)],
    session: AsyncSession = Depends(
        db_helper.get_session,
    ),
) -> UserResponse:
    result = await user_service.delete(user_id, session)
    return result

@router.patch("/update")
async def update_user(
    session: Annotated[AsyncSession,Depends(db_helper.get_session)],
    user_service: Annotated[UserService,Depends(user_service)],
    request: Request,
    schema: UserUpdate,
)->UserResponse:
    payload = decode_jwt(request.cookies.get('access_token'))
    result = await user_service.update(schema,session,payload)
    return result 
    