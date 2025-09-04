from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession
import aiohttp
import jwt
from typing import Dict
from fastapi import status,HTTPException

from auth.utils import create_token, decode_jwt, encode_jwt
from config import settings
from schemas.profiles.profile import UpdateProfile
from schemas.token.token import TokenInfo
from schemas.user.user import UserLogin, UserRegistration
from utils.auth_repository import AbstractAuthRepository
from services.profile import ProfileService
from redis_service.redis_profile_service import RedisJSONProfileService

class AuthService:

    def __init__(self, auth_repository: AbstractAuthRepository) -> TokenInfo:

        self.auth_repository = auth_repository()

    async def get_refresh_token(self, user_data: dict):

        payload = {
            "sub": user_data.username,
            "email": user_data.email,
            "token_type": settings.auth_jwt.REFRESH_TOKEN_TYPE,
            "user_id": user_data.id
        }

        refresh_token = encode_jwt(payload)

        return TokenInfo(refresh_token=refresh_token)

    async def check_refresh_token(self, refresh_token: str, session: AsyncSession):

        payload = decode_jwt(refresh_token)
        result = await self.auth_repository.check_refresh_token(payload, session)

        return result

    async def register_user(
        self,
        schema: UserRegistration, 
        session: AsyncSession,
        profile_service: ProfileService,
        redis_service: RedisJSONProfileService,
    ) -> Tuple[str, str]:
        
        
            
        user_data = schema.model_dump()
        result = await self.auth_repository.register_user(user_data, session)

        refresh_token = create_token(result.username, result.email, "refresh", result.id)
        access_token = create_token(result.username, result.email, "access", result.id)

        temporary_profile = UpdateProfile(username=result.username)
        profile = await profile_service.update_profile(session, refresh_token, temporary_profile, redis_service)

        user_session = await self.create_user_session(refresh_token, session)

        return refresh_token, access_token
                     
    
    async def create_user_session(self, refresh_token: str, session: AsyncSession):

        payload = decode_jwt(refresh_token)
        result = await self.auth_repository.create_user_session(
            refresh_token, payload, session
        )

        return result

    async def get_tokens_with_google(self, email: str, session: AsyncSession):

        result = await self.auth_repository.get_tokens_with_google(email, session)

        return result

    async def get_google_user_data(self,code: str)->Dict:

        google_token_url = settings.auth_jwt.google_token_url

        async with aiohttp.ClientSession() as g_session:
            async with g_session.post(
                url=google_token_url,
                data={
                    "client_id": settings.auth_jwt.google_client_id,
                    "client_secret": settings.auth_jwt.google_client_secret,
                    "grant_type": "authorization_code",
                    "redirect_uri": "http://localhost:3000/home",
                    "code": code,
                },
                ssl=False,
            ) as g_response:
                res = await g_response.json()
                id_token = res["id_token"]
                user_data = jwt.decode(
                    id_token,
                    algorithms=["RS256"],
                    options={"verify_signature": False},
                )
            return user_data

    async def login_user(self, schema: UserLogin, session: AsyncSession):

        user_data = schema.model_dump()
        result = await self.auth_repository.login_user(user_data, session)

        return result

    async def get_user_id(self, refresh_token: str, session: AsyncSession):

        return await self.auth_repository.get_user_id(refresh_token, session)

    async def refresh_token(self, session: AsyncSession, refresh_token: str):

        result = await self.auth_repository.refresh_token(session, refresh_token)

        return result

   