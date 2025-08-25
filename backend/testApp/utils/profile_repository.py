from abc import ABC, abstractmethod
from models.profiles import Profile
from abc import ABC, abstractmethod
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from models.user import User
from models.profiles import Profile
from models.file import UserPhoto
from schemas.profiles.profile import Profile as ProfileSchema


class AbstractProfileRepository(ABC):

    @abstractmethod
    async def get_user_profile(self):
        raise NotImplementedError


class SQLAlchemyProfileRepository(AbstractProfileRepository):

    model = Profile

    async def get_user_profile(self, session: AsyncSession, email: str):
        stmt = select(User).where(User.email == email)
        async with session as session:
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is None:
                raise HTTPException(status_code=400, detail="Not such user")
            user_id = user.id
            stmt = select(self.model).where(self.model.user_id == user_id)
            result = await session.execute(stmt)
            stmt = select(UserPhoto.url).where(UserPhoto.user_id == user_id)
            photo = await session.execute(stmt)
            url = photo.scalar_one_or_none()
            profile = result.scalar_one_or_none()
            result = {**profile.__dict__}
            result = {k: v for k, v in result.items() if not k.startswith("_")}
            result["profile_photo_url"] = url
        return result

    async def update_profile(
        self, session: AsyncSession, email: str, profile_data: dict
    ):
        try:
            stmt = select(User).where(User.email == email)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            if user is None:
                raise HTTPException(status_code=404, detail="User not found")

            stmt = select(self.model).where(self.model.user_id == user.id)
            result = await session.execute(stmt)
            profile = result.scalar_one_or_none()

            if profile is None:
                profile_data["user_id"] = user.id
                stmt = insert(self.model).values(**profile_data).returning(self.model)
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
                status_code=400, detail=f"Failed to update profile: {str(e)}"
            )

    async def create_profile(
        self, session: AsyncSession, email: str, profile_data: dict
    ):
        
        stmt = select(User).where(User.email == email)
        async with session as session:
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is None:
                raise HTTPException(status_code=400, detail="Not such user")
            profile_data["user_id"] = user.id
            stmt = insert(self.model).values(**profile_data).returning(self.model)
            result = await session.execute(stmt)
            profile = result.scalar_one_or_none()

            await session.commit()
            await session.refresh(profile)

        return profile

    async def set_user_profile_photo(
        self, user_id: int, data_dict: dict, session: AsyncSession
    ):
        stmt = select(self.model.id).where(self.model.user_id == user_id)
        try:
            async with session as session:
                result = await session.execute(stmt)
                profile_id = result.scalar_one_or_none()
                values = {
                    "profile_id": profile_id,
                    "user_id": user_id,
                    "s3_key": data_dict["s3_key"],
                    "filename": data_dict["filename"],
                    "url": data_dict["file_url"],
                }

                stmt = select(UserPhoto).where(UserPhoto.user_id == user_id)
                photo = await session.execute(stmt)
                user_photo = photo.scalar_one_or_none()
                if user_photo is None:
                    stmt = insert(UserPhoto).values(**values).returning(UserPhoto)
                    result = await session.execute(stmt)
                    user_photo = result.scalar_one()
                else:
                    for field, value in values.items():
                        if hasattr(user_photo, field):
                            setattr(user_photo, field, value)
                    session.add(user_photo)
                await session.commit()
                await session.refresh(user_photo)

                return user_photo

        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Failed to set photo: {str(e)}"
            )
