from typing import List
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import decode_jwt
from config import settings
from schemas.token.token import TokenInfo
from utils.profile_repository import AbstractProfileRepository
from s3.s3_client import s3_client
from repository.auth import AuthRepository
from redis_service.redis_profile_service import RedisJSONProfileService


class ProfileService:

    def __init__(self, profile_repository: AbstractProfileRepository):

        self.profile_repository = profile_repository()

    async def upload_user_profile_photo(
        self,
        auth_repository: AuthRepository,
        refresh_token: str,
        session: AsyncSession,
        file: UploadFile,
        folder: str,
    ):
        user_id = await auth_repository.get_user_id(refresh_token, session)
        result = await s3_client.upload_file_from_uploadfile(user_id, file, folder)
        photo = await self.profile_repository.set_user_profile_photo(
            user_id, result, session
        )

        return result
    
    async def search_users_profiles(
        self, session: AsyncSession, search_filter: str, payload: str
    ):
        users_profiles = await self.profile_repository.search_users_profiles(session, search_filter, payload)
        return users_profiles
    
    async def get_user_profile(
        self,
        user_id: int,
        session: AsyncSession,
        redis_service: RedisJSONProfileService,
        refresh_token: str,
    ):

        # payload = decode_jwt(refresh_token)
        # email = payload["email"]
        # user_id = payload["user_id"]

        # redis_result = await redis_service.get_profile(user_id)
        # if redis_result is None:
            # result = await self.profile_repository.get_user_profile(session, email)
        result = await self.profile_repository.get_user_profile(session, user_id)

        profile = await redis_service.create_profile(user_id, result)
        return result
        # else:
        #     return redis_result

    async def get_user_profiles(
        self,
        user_ids: List[int],
        redis_service: RedisJSONProfileService,
        session: AsyncSession,
    ):
        try:
            redis_results = await redis_service.get_profiles_pipeline(user_ids)
            missing_user_ids = []
            results_map = {}

            for user_id, redis_result in zip(user_ids, redis_results):
                if redis_result is None:
                    missing_user_ids.append(user_id)
                else:
                    results_map[user_id] = redis_result
            if missing_user_ids:
                db_results = await self.profile_repository.get_user_profiles(
                    missing_user_ids, session
                )

                if db_results:
                    await redis_service.create_profiles_pipeline(db_results)
                    results_map.update(db_results)

                for user_id in missing_user_ids:
                    if user_id not in results_map:
                        results_map[user_id] = None

            return [results_map.get(user_id) for user_id in user_ids]
        except Exception as e:
            return await self.profile_repository.get_user_profiles(user_ids, session)

    async def update_profile(
        self,
        session: AsyncSession,
        refresh_token: str,
        schema: dict,
        redis_service: RedisJSONProfileService,
    ):

        profile_data = schema.model_dump(exclude_unset=True)
        payload = decode_jwt(refresh_token)
        email = payload["email"]
        user_id = payload["user_id"]


        try:
            result = await self.profile_repository.update_profile(
            session, email, profile_data
        )
            redis_profile = await redis_service.update_profile(user_id, profile_data)
            if not redis_profile:
                user_data = result.copy()
                user_data.pop("_sa_instance_state", None)
                redis_profile = await redis_service.create_profile(user_id, user_data)
            return result

        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to update profile: {str(e)}"
            )

    async def create_profile(
        self, session: AsyncSession, refresh_token: str, schema: dict
    ):
        profile_data = schema.model_dump()
        payload = decode_jwt(refresh_token)
        email = payload["email"]
        result = await self.profile_repository.create_profile(
            session, email, profile_data
        )

        return result

    async def get_habits(self, refresh_token: str, session: AsyncSession):
        payload = decode_jwt(refresh_token)
        result = await self.profile_repository.get_habits(session)
        return result
