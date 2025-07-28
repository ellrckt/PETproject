from utils.repository import AbstractRepository
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user.user import UserRegistration, UserLogin,UserUpdate


class UserService:

    def __init__(self, user_repo: AbstractRepository):
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

    async def update(self,schema: UserUpdate,session: AsyncSession,payload: dict):
        
        user_dict = schema.model_dump()
        result = await self.user_repo.update(user_dict,session,payload)
        return result

    async def register_user(self, schema: UserRegistration, session: AsyncSession):
        user_data = schema.model_dump()
        result = await self.user_repo.register_user(user_data, session)
        return result

    async def login_user(self, schema: UserLogin, session: AsyncSession):
        user_data = schema.model_dump()
        result = await self.user_repo.login_user(user_data, session)
        return result
