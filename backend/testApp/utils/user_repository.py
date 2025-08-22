from abc import ABC, abstractmethod
from db.db import db_helper
from sqlalchemy import select, insert, update,func
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException,Request, Response

from models.habits import Habits
from auth.utils import hash_password, validate_password, encode_jwt, decode_jwt
from schemas.token.token import TokenInfo
from datetime import datetime
from models.user import User
from models.session import UserSession
from models.location import UserLocation
from models.profiles import Profile
from datetime import timedelta,datetime
from schemas.user.user import UserCityCountry


ACCESS_TOKEN_TYPE = "access_token"
REFRESH_TOKEN_TYPE = "refresh_token"


class AbstractUserCRUDRepository(ABC):

    @abstractmethod
    async def add_one(data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_all():
        raise NotImplementedError

    @abstractmethod
    async def update():
        raise NotImplementedError

    @abstractmethod
    async def delete():
        return NotImplementedError


class SQLAlchemyUserCRUDRepository(AbstractUserCRUDRepository):

    model = User

    async def add_one(self, data: dict, session: AsyncSession):
        async with session as session:
            data["password"] = hash_password(data["password"])
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            user_instance = res.scalar_one()
            return user_instance
        
    async def get_user_by_email(self,session: AsyncSession,email: str):
        async with  session as session:
            stmt = select(self.model).where(self.model.email == email)
            user = await session.execute(stmt)
            if user is None:
                raise HTTPException(status_code=401, detail="Invalid email")
            pass


    async def get_all(self, session: AsyncSession):
        async with session as session:
            stmt = select(self.model)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def delete(self, user_id: int, session: AsyncSession):
        async with session as session:
            stmt = select(self.model).where(self.model.id == user_id)
            result = await session.execute(stmt)
            user_instance = result.scalar_one_or_none()

            if user_instance:
                await session.delete(user_instance)
                await session.commit()
                return user_instance
            return None

    async def update(self, user_data: dict, session: AsyncSession, payload: dict):
        async with session.begin():

            stmt = select(self.model).where(self.model.email == payload["email"])
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            if user is None:
                raise HTTPException(status_code=401, detail="Invalid email")

            if not user.is_active:
                raise HTTPException(status_code=403, detail="User inactive")

            for key, value in user_data.items():
                if value is not None:
                    setattr(user, key, value)

            session.add(user)
            await session.commit()

        return user


class AbstractUserRepository(ABC):

    model = User

    @abstractmethod
    async def login_user():
        return NotImplementedError

    @abstractmethod
    async def register_user():
        return NotImplementedError

    @abstractmethod
    async def refresh_token():
        return NotImplementedError


class SQLAlchemyUserRepository(AbstractUserRepository):

    model = User

    async def check_refresh_token(self, payload: dict):
        stmt = select(self.model).where(self.model.email == payload["email"])
        async with session as session:
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
        stmt = select(UserSession.refresh_token).where(UserSession.user_id == user.id)
        async with session as session:
            result = await session.execute(stmt)
            session = result.scalar_one_or_none()
        if session is None:
            raise HTTPException(status_code = 403, detail = "Refresh token is missing")
        return True

    async def get_hobbies(self,session: AsyncSession):
        async with session as session:
            stmt = select(Habits)
            result = await session.execute(stmt)
            hobbies = result.scalars().all()
        
        return hobbies
    
    async def get_user_profile(self,session: AsyncSession,email: str):
        stmt = select(self.model).where(self.model.email == email)
        async with session as session:
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is  None:
                    raise HTTPException(
                        status_code=400, detail="Not such user"
                    )
            user_id = user.id
            stmt = select(Profile).where(Profile.user_id == user_id)
            result = await session.execute(stmt)
            profile = result.scalar_one_or_none()

        return profile
    
    async def update_profile(self, session: AsyncSession, email: str, profile_data: dict):
        try:
            stmt = select(self.model).where(self.model.email == email)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            
            if user is None:
                raise HTTPException(
                    status_code=404, 
                    detail="User not found"
                )

            stmt = select(Profile).where(Profile.user_id == user.id)
            result = await session.execute(stmt)
            profile = result.scalar_one_or_none()

            if profile is None:
                profile_data["user_id"] = user.id
                stmt = insert(Profile).values(**profile_data).returning(Profile)
                result = await session.execute(stmt)
                profile = result.scalar_one()
            else:
                for field, value in profile_data.items():
                    if hasattr(profile, field):  
                        setattr(profile, field, value)

            await session.commit()
            await session.refresh(profile)
            
            return profile

        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Failed to update profile: {str(e)}"
            )
    
    async def create_profile(self,session: AsyncSession,email: str,profile_data: dict):
        stmt = select(self.model).where(self.model.email == email)
        async with session as session:
            result = await session.execute(stmt) 
            user = result.scalar_one_or_none()
            if user is  None:
                    raise HTTPException(
                        status_code=400, detail="Not such user"
                    )
            profile_data["user_id"] = user.id
            stmt = insert(Profile).values(**profile_data).returning(Profile)
            result = await session.execute(stmt)
            profile = result.scalar_one_or_none()
            
            await session.commit()
            await session.refresh(profile)
    
        return profile


    async def register_user(self, user_data: dict, session: AsyncSession):

        async with session.begin():
            if len(user_data["email"])==0:
                raise HTTPException(status_code = 400, detail = "Email is required")
            else:
                stmt = select(self.model).where(self.model.email == user_data["email"])
                result = await session.execute(stmt)
                user = result.scalar_one_or_none()
                if user is not None:
                    raise HTTPException(
                        status_code=400, detail="User with this email is already exists."
                    )
                else:
                    if user_data['password'] == user_data['repit_password']:
                            if len(user_data["password"])>=4:
                                user_data["password"] = hash_password(user_data["password"])
                                del user_data["repit_password"]
                                stmt = insert(self.model).values(**user_data).returning(self.model)
                                result = await session.execute(stmt)
                                await session.commit()
                                new_user = result.scalar_one_or_none()
                            else:
                                raise HTTPException(status_code = 422,detail = "Password must be at least 4 characters long")
                    else:
                        raise HTTPException(
                            status_code = 422,detail = "Passwords do not match"
                        )
        return new_user

    async def create_user_session(self,refresh_token: str, payload: dict, session: AsyncSession):
        stmt = select(self.model).where(self.model.email==payload["email"])
        async with session as session:
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

        new_session = UserSession(
            user_id=user.id,
            refresh_token= refresh_token,
            exp=datetime.fromtimestamp(payload["exp"]), 
            iat=datetime.fromtimestamp(payload["iat"]),
            is_blacklisted=False)
        

        async with session:
            stmt = select(UserSession).where(UserSession.user_id == user.id)
            result = await session.execute(stmt)
            old_session = result.scalar_one_or_none()
            if old_session is None:
                stmt = insert(UserSession).values(
                    user_id=new_session.user_id,
                    refresh_token=new_session.refresh_token,
                    exp=new_session.exp,iat=new_session.iat,
                    is_blacklisted=new_session.is_blacklisted).returning(UserSession)
                result = await session.execute(stmt)
                new_session = result.scalar_one_or_none()
           
            await session.commit() 
            await session.refresh(new_session)  
            
        return new_session

    async def login_user(self, data_dict: dict, session: AsyncSession)->TokenInfo:

        async with session as session:
            stmt = select(self.model).where(self.model.email == data_dict["email"])
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is None:
                raise HTTPException(status_code=401, detail="Invalid email")
            if len(data_dict["password"]) >= 4:
                check_pass = validate_password(data_dict["password"], user.password)
                if not check_pass:
                    raise HTTPException(status_code=401, detail="Invalid password.")
                if not user.is_active:
                    raise HTTPException(status_code=403, detail="user inactive")
                payload = {
                    "sub": user.username,
                    "email": user.email,
                    "token_type": REFRESH_TOKEN_TYPE,
                }
                refresh_token = encode_jwt(payload)
            else:  
                raise HTTPException(status_code = 422,detail = "Password must be at least 4 characters long")
            return TokenInfo(refresh_token=refresh_token)
            # return TokenInfo(access_token=access_token, refresh_token=refresh_token)

    async def refresh_token(
        self, session: AsyncSession, refresh_token: str
    ):
        print(refresh_token)
        access_payload = decode_jwt(refresh_token)
        async with session as session:
            stmt = select(self.model).where(self.model.email == access_payload["email"].lower())
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is None:
                raise HTTPException(status_code=401, detail="invalid email")
            if user:
                if user.is_active == "False":
                    raise HTTPException(status_code=403, detail="user innactive")

                payload_to_new_token = access_payload
                payload_to_new_token["token_type"] = ACCESS_TOKEN_TYPE
                access_token = encode_jwt(payload_to_new_token)
            return access_token
    
        
    async def get_tokens_with_google(self, email: str,session: AsyncSession):
        async with session as session:
            stmt = select(self.model).where(self.model.email == email)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            if user is None:
                raise HTTPException(status_code=401, detail="Invalid email")

            if not user.is_active:
                raise HTTPException(status_code=403, detail="User inactive")
            user_id  = user.id
            stmt = select(UserSession.refresh_token).where(UserSession.user_id == user_id)
            result = await session.execute(stmt)
            refresh_token = result.scalar_one_or_none()
            
            return TokenInfo(refresh_token = refresh_token)

    async def set_user_location(self,location: dict, session: AsyncSession, email: str,city: str, country: str)->UserCityCountry:
        async with session as session:
            stmt = select(self.model).where(self.model.email == email)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is None:
                raise HTTPException(status_code=401, detail="Invalid email")

            if not user.is_active:
                raise HTTPException(status_code=403, detail="User inactive")
            user_id = user.id

            stmt = insert(UserLocation).values(
                user_id = user_id,
                geom=func.ST_MakePoint(location['lng'],location['lat']),
                city = city,
                country = country
            )
            result = await session.execute(stmt)
            await session.commit()
            return UserCityCountry(city = city,country = country)


    async def set_user_lat_lng(self,location: dict,session: AsyncSession, email: str, city: str, country: str)-> UserCityCountry:
            result = await self.set_user_location(location,session,email,city,country)
            return result
