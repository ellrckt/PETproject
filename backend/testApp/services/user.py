from utils.user_repository import AbstractUserCRUDRepository,AbstractUserRepository
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user.user import UserRegistration, UserLogin, UserUpdate,UserEmailConffirmation
from auth.utils import decode_jwt
# from simplegmail import Gmail
import random
import string
from fastapi import Response 

class UserCRUDService:

    def __init__(self, user_repo: AbstractUserCRUDRepository):
        self.user_repo = user_repo()

    async def add_one(self, user_schema: User, session: AsyncSession):
        user_dict = user_schema.model_dump()
        user_id = await self.user_repo.add_one(user_dict, session)
        return user_id

    async def get_all(self, session: AsyncSession):

        result = await self.user_repo.get_all(session)
        return result

    async def delete(self, user_id: int, session: AsyncSession):

        result = await self.user_repo.delete(user_id, session)
        return result

    async def update(self, schema: UserUpdate, session: AsyncSession, payload: dict):

        user_dict = schema.model_dump()
        result = await self.user_repo.update(user_dict, session, payload)
        return result





class UserService:

    def __init__(self, user_repo: AbstractUserRepository):
        self.user_repo = user_repo()

    async def register_user(self, schema: UserRegistration, session: AsyncSession):
        user_data = schema.model_dump()
        result = await self.user_repo.register_user(user_data, session)
        return result
    
    async def create_user_session(self,user: User, refresh_token: str, session: AsyncSession):
        payload = decode_jwt(refresh_token)
        result = await self.user_repo.create_user_session(user,payload,session)
        return result
    
    async def get_tokens_with_google(self, email: str,session: AsyncSession):

        result = await self.user_repo.get_tokens_with_google(email, session)
        return result

    async def login_user(self, schema: UserLogin, session: AsyncSession):
        user_data = schema.model_dump()
        result = await self.user_repo.login_user(user_data, session)
        return result

    async def refresh_token(
        self, session: AsyncSession, refresh_token: str
    ):
        result = await self.user_repo.refresh_token(session, refresh_token)
        return result

    async def get_user_location(self,schema: dict, session: AsyncSession,response: Response):
        location = schema.model_dump()
        result = await self.user_repo.get_user_location(location, session, response)
        return result
