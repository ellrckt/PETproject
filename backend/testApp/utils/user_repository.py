from abc import ABC, abstractmethod
from db.db import db_helper
from sqlalchemy import select, insert,update
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from auth.utils import hash_password, validate_password, encode_jwt, decode_jwt
from schemas.token.token import TokenInfo
from datetime import datetime
from models.user import User

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

    async def register_user(self, user_data: dict, session: AsyncSession):

        async with session.begin():
            stmt = select(self.model).where(self.model.email == user_data["email"])
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is not None:
                raise HTTPException(
                    status_code=400, detail="User with this email is already exists."
                )
            else:
                user_data["password"] = hash_password(user_data["password"])
                del user_data["repit_password"]
                stmt = insert(self.model).values(**user_data).returning(self.model)
                result = await session.execute(stmt)
                await session.commit()
                new_user = result.scalar_one_or_none()
        return new_user

    async def login_user(self, data_dict: dict, session: AsyncSession):

        async with session as session:
            stmt = select(self.model).where(self.model.email == data_dict["email"])
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is None:
                raise HTTPException(status_code=401, detail="Invalid email")
            check_pass = validate_password(data_dict["password"], user.password)
            if not check_pass:
                raise HTTPException(status_code=401, detail="Invalid password.")
            if not user.is_active:
                raise HTTPException(status_code=403, detail="user inactive")
            payload = {
                "sub": user.username,
                "email": user.email,
                "token_type": ACCESS_TOKEN_TYPE,
            }
            access_token = encode_jwt(payload)
            refresh_token = encode_jwt(
                {
                    "sub": user.username,
                    "email": user.email,
                    "token_type": REFRESH_TOKEN_TYPE,
                }
            )
            return TokenInfo(access_token=access_token, refresh_token=refresh_token)
            # return TokenInfo(access_token=access_token, refresh_token=refresh_token)

    async def refresh_token(
        self, access_token: str, session: AsyncSession, refresh_token: str
    ):

        access_payload = decode_jwt(refresh_token)
        async with session as session:
            stmt = select(self.model).where(self.model.email == access_payload["email"])
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
    
    # async def confirm_email(
    #     self,
    #     session: AsyncSession,
    #     code_data: dict,
    #     data_dict: dict
    # ):
    #     if code_data["confirmation_code"] == code_data["typed_code"]:

    #         async with session:
    #             stmt = select(self.model).where(self.model.email == data_dict["email"])
    #             result = await session.execute(stmt)
    #             user = result.scalar_one_or_none()

    #             if user is None:
    #                 raise HTTPException(status_code=401, detail="Invalid email")

    #             if not user.is_active:
    #                 raise HTTPException(status_code=403, detail="User inactive")

    #             stmt_update = (
    #                 update(self.model).where(self.model.email == data_dict["email"]).values(email_is_confirmed=True)
    #             )
    #             await session.execute(stmt_update)
    #             await session.commit()
    #         return user.email_is_confirmed
