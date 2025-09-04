from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy import select, insert, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from db.db import db_helper
from auth.utils import hash_password, validate_password, encode_jwt, decode_jwt
from schemas.token.token import TokenInfo
from models.user import User
from models.session import UserSession
from config import settings 


class AbstractAuthRepository(ABC):

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


class SQLAlchemyAuthRepository(AbstractAuthRepository):

    model = User

    async def check_refresh_token(self, payload: dict, session: AsyncSession):
        
        async with session as session:
            stmt = select(self.model).where(self.model.email == payload["email"])
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            stmt = select(UserSession.refresh_token).where(UserSession.user_id == user.id)
            result = await session.execute(stmt)
            session = result.scalar_one_or_none()
            if session is None:
                raise HTTPException(status_code=401, detail="Refresh token is missing")

    async def register_user(self, user_data: dict, session: AsyncSession):
        async with session.begin():
            if len(user_data["email"]) == 0:
                raise HTTPException(status_code=400, detail="Email is required")
            else:
                stmt = select(self.model).where(self.model.email == user_data["email"])
                result = await session.execute(stmt)
                user = result.scalar_one_or_none()

                if user is not None:
                    raise HTTPException(
                        status_code=400,
                        detail="User with this email is already exists.",
                    )
                else:
                    if user_data["password"] == user_data["repit_password"]:
                        if len(user_data["password"]) >= 4:
                            user_data["password"] = hash_password(user_data["password"])
                            del user_data["repit_password"]
                            stmt = (
                                insert(self.model)
                                .values(**user_data)
                                .returning(self.model)
                            )
                            result = await session.execute(stmt)
                            await session.commit()
                            new_user = result.scalar_one_or_none()
                        else:
                            raise HTTPException(
                                status_code=422,
                                detail="Password must be at least 4 characters long",
                            )
                    else:
                        raise HTTPException(
                            status_code=422, detail="Passwords do not match"
                        )
        return new_user

    async def create_user_session(
        self, refresh_token: str, 
        payload: dict, 
        session: AsyncSession
    ):

        async with session as session:
            stmt = select(self.model).where(self.model.email == payload["email"])
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            stmt = select(UserSession).where(UserSession.user_id == user.id)
            result = await session.execute(stmt)
            old_session = result.scalar_one_or_none()

            if old_session:
                old_session.refresh_token = refresh_token
                old_session.exp = datetime.fromtimestamp(payload["exp"])
                old_session.iat = datetime.fromtimestamp(payload["iat"])
                old_session.is_blacklisted = False
                await session.commit()
                await session.refresh(old_session)
                return old_session.refresh_token
            else:
                new_session = UserSession(
                    user_id=user.id,
                    refresh_token=refresh_token,
                    exp=datetime.fromtimestamp(payload["exp"]),
                    iat=datetime.fromtimestamp(payload["iat"]),
                    is_blacklisted=False,
                )
                session.add(new_session)  
                await session.commit()
                await session.refresh(new_session) 
                return new_session.refresh_token

            
    async def login_user(self, data_dict: dict, session: AsyncSession) -> TokenInfo:

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
                    "token_type": settings.auth_jwt.REFRESH_TOKEN_TYPE,
                    "user_id": user.id
                }
                refresh_token = encode_jwt(payload)
            else:
                raise HTTPException(
                    status_code=422,
                    detail="Password must be at least 4 characters long",
                )
            return TokenInfo(refresh_token=refresh_token)

    async def refresh_token(self, session: AsyncSession, refresh_token: str):
        access_payload = decode_jwt(refresh_token)
        async with session as session:
            stmt = select(self.model).where(
                self.model.email == access_payload["email"].lower()
            )
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is None:
                raise HTTPException(status_code=401, detail="invalid email")
            if user:
                if user.is_active == "False":
                    raise HTTPException(status_code=403, detail="user innactive")

                payload_to_new_token = access_payload
                payload_to_new_token["token_type"] = settings.auth_jwt.ACCESS_TOKEN_TYPE
                access_token = encode_jwt(payload_to_new_token)
            return access_token

    async def get_tokens_with_google(self, email: str, session: AsyncSession):
        async with session as session:
            stmt = select(self.model).where(self.model.email == email)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            if user is None:
                raise HTTPException(status_code=401, detail="Invalid email")

            if not user.is_active:
                raise HTTPException(status_code=403, detail="User inactive")
            user_id = user.id

            stmt = select(UserSession.refresh_token).where(
                UserSession.user_id == user_id
            )
            result = await session.execute(stmt)
            refresh_token = result.scalar_one_or_none()
            if refresh_token is None:
                raise HTTPException(status_code=505, detail="Missed user session")
            
            return TokenInfo(refresh_token=refresh_token)

    async def get_refresh_token(self, refresh_token: str):
        return refresh_token

    async def get_user_id(self, refresh_token: str, session: AsyncSession):

        email = decode_jwt(refresh_token)["email"]
        async with session as session:
            stmt = select(self.model).where(self.model.email == email)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            user_id = user.id
            
        return user_id