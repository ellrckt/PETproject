
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import decode_jwt
from config import settings

from schemas.token.token import TokenInfo
from utils.profile_repository import AbstractProfileRepository
from s3.s3_client import s3_client
from repository.auth import AuthRepository

class ProfileService:

    def __init__(self, profile_repository: AbstractProfileRepository) -> TokenInfo:

        self.profile_repository = profile_repository()

    async def upload_user_profile_photo(
        self, 
        auth_repository: AuthRepository, 
        refresh_token: str, 
        session: AsyncSession, 
        file: UploadFile, 
        folder: str
    ):
        
        user_id = await auth_repository.get_user_id(refresh_token, session)
        result = await s3_client.upload_file_from_uploadfile(user_id, file, folder)
        photo = await self.profile_repository.set_user_profile_photo(user_id, result, session)

        return result

    async def get_user_profile(self, session: AsyncSession, refresh_token: str):

        payload = decode_jwt(refresh_token)
        email = payload["email"]

        result = await self.profile_repository.get_user_profile(session, email)

        return result

    async def update_profile(
        self,
        session: AsyncSession, 
        refresh_token: str, 
        schema: dict
    ):
        
        profile_data = schema.model_dump(exclude_unset=True)
        payload = decode_jwt(refresh_token)
        email = payload["email"]
        
        result = await self.profile_repository.update_profile(session, email, profile_data)

        return result

    async def create_profile(
        self, session: AsyncSession, 
        refresh_token: str, 
        schema: dict
    ):
        profile_data = schema.model_dump()
        payload = decode_jwt(refresh_token)
        email = payload["email"]

        result = await self.profile_repository.create_profile(session, email, profile_data)
        
        return result

