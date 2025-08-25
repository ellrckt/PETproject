from typing import Tuple

from fastapi import Request, UploadFile
from geopy.geocoders import Nominatim
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import create_token, decode_jwt, encode_jwt
from config import settings
from models.user import User
from schemas.profiles.profile import UpdateProfile
from schemas.token.token import TokenInfo
from schemas.user.user import UserLogin, UserRegistration, UserUpdate
from utils.user_repository import AbstractUserCRUDRepository, AbstractUserRepository
from s3.s3_client import s3_client


class UserCRUDService:

    def __init__(self, user_repository: AbstractUserCRUDRepository):
        self.user_repository = user_repository()

    async def add_one(self, user_schema: User, session: AsyncSession):
        user_dict = user_schema.model_dump()
        user_id = await self.user_repository.add_one(user_dict, session)
        return user_id

    async def get_all(self, session: AsyncSession):

        result = await self.user_repository.get_all(session)
        return result

    async def delete(self, user_id: int, session: AsyncSession):

        result = await self.user_repository.delete(user_id, session)
        return result

    async def update(self, schema: UserUpdate, session: AsyncSession, payload: dict):

        user_dict = schema.model_dump()
        result = await self.user_repository.update(user_dict, session, payload)
        return result

    async def get_user_by_email(self, session: AsyncSession, email: str):

        result = await self.user_repository.get_user_by_email(session, email)
        return result


class UserService:

    def __init__(self, user_repository: AbstractUserRepository) -> TokenInfo:

        self.user_repository = user_repository()

   