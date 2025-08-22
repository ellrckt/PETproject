from utils.user_repository import AbstractUserCRUDRepository,AbstractUserRepository
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user.user import UserRegistration, UserLogin, UserUpdate
from auth.utils import decode_jwt
# from simplegmail import Gmail
import random
import string
from fastapi import Response ,Request
from geopy.geocoders import Nominatim

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

    async def get_user_by_email(self,session: AsyncSession, email: str):

        result = await self.user_repo.get_user_by_email(session, email)
        return result





class UserService:

    def __init__(self, user_repo: AbstractUserRepository):
        self.user_repo = user_repo()

    async def check_jwt(self, refresh_token: str):
        payload = decode_jwt(refresh_token)
        result = await self.user_repo.check_jwt(payload)
        return result
    
    async def register_user(self, schema: UserRegistration, session: AsyncSession):
        user_data = schema.model_dump()
        result = await self.user_repo.register_user(user_data, session)
        return result
    
    async def create_user_session(self, refresh_token: str, session: AsyncSession):
        payload = decode_jwt(refresh_token)
        result = await self.user_repo.create_user_session(refresh_token, payload,session)
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

    async def get_city_country(self,location: dict):
        latitude = location['lat'] 
        longitude = location['lng']
        geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 OPR/120.0.0.0")
        location = geolocator.reverse(f"{latitude}, {longitude}", exactly_one=True, language='en')
        
        if location:
            address = location.raw.get('address', {})
            country = address.get('country', '')
            city = address.get('city', '') or address.get('town', '') or address.get('village', '')
            return city, country
        return None, None


    async def set_user_lat_lng(self,schema: dict, session: AsyncSession,request: Request):
        location = schema.model_dump()
        refresh_token = request.cookies.get("refresh_token")
        payload = decode_jwt(refresh_token)
        email = payload["email"]
        city,country = await self.get_city_country(location)
        result = await self.user_repo.set_user_lat_lng(location, session, email,city,country)
        
        return result
    
    async def get_hobbies(self,session: AsyncSession):
        result = await self.user_repo.get_hobbies(session)
        hobbies_list = [hobby.name for hobby in result]
        return hobbies_list
    
    async def get_user_profile(self,session: AsyncSession,refresh_token: str):
        payload = decode_jwt(refresh_token)
        email = payload["email"]
        result = await self.user_repo.get_user_profile(session,email)
        return result

    async def update_profile(self,session: AsyncSession,refresh_token: str,schema: dict):
        profile_data = schema.model_dump(exclude_unset = True)
        payload = decode_jwt(refresh_token)
        email = payload["email"]
        result = await self.user_repo.update_profile(session,email,profile_data)
        return result

    async def create_profile(self,session: AsyncSession,refresh_token: str,schema: dict):
        profile_data = schema.model_dump()
        payload = decode_jwt(refresh_token)
        email = payload["email"]
        result = await self.user_repo.create_profile(session,email,profile_data)
        return result

