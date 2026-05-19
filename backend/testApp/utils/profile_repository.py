from abc import ABC, abstractmethod
from models.profiles import Profile
from abc import ABC, abstractmethod
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from typing import List

from models.user import User
from schemas.profiles.profile import Profile as ProfileSchema
from models.habits import Habits
from models.file import UserPhoto
from schemas.profiles.profile import Profile as ProfileSchema


class AbstractProfileRepository(ABC):

    @abstractmethod
    async def get_user_profile(self):
        raise NotImplementedError


class SQLAlchemyProfileRepository(AbstractProfileRepository):
    model = Profile

    async def get_user_profile(self, session: AsyncSession, user_id: int):
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await session.execute(stmt)
        profile = result.scalar_one_or_none()
        
        if profile is None:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        stmt = select(UserPhoto.url).where(UserPhoto.user_id==user_id)
        result = await session.execute(stmt)
        photo_url = result.scalar_one_or_none()
        profile_dict = {
            "id": profile.id,
            "user_id": profile.user_id,
            "username": profile.username,
            "age": profile.age,
            "city": profile.city,
            "country": profile.country,
            "about_user": profile.about_user,
            "user_habits": profile.user_habits,
            "profile_photo_url": photo_url,
        }
        return profile_dict
        

    async def get_user_profiles(
        self, user_ids: int, session: AsyncSession
    ) -> List[dict]:
        if not user_ids:
            return []

        stmt = (
            select(self.model, UserPhoto.url)
            .outerjoin(UserPhoto, self.model.user_id == UserPhoto.user_id)
            .where(self.model.user_id.in_(user_ids))
        )
        result = await session.execute(stmt)
        profiles_list = []
        for profile, photo_url in result:
            profiles_list.append({
                "id": profile.id,
                "user_id": profile.user_id,
                "username": profile.username,
                "age": profile.age,
                "city": profile.city,
                "country": profile.country,
                "about_user": profile.about_user,
                "profile_photo_url": photo_url, 
            })

        return profiles_list
        
    async def search_users_profiles(self, session: AsyncSession, search_filter: str, payload: dict)->List[ProfileSchema]:
        stmt = select(Profile).filter(
            Profile.username.ilike(f"%{search_filter}%"),
            Profile.user_id != payload["user_id"])
        users_profiles = await session.execute(stmt)
        result = users_profiles.scalars()
        return result
        

    async def update_profile(
        self, session: AsyncSession, email: str, profile_data: dict
    )-> dict:
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
            stmt = select(UserPhoto.url).where(UserPhoto.user_id==user.id)
            result = await session.execute(stmt)
            photo_url = result.scalar_one_or_none()
            profile_dict = {
                "id": profile.id,
                "user_id": profile.user_id,
                "username": profile.username,
                "age": profile.age,
                "city": profile.city,
                "country": profile.country,
                "about_user": profile.about_user,
                "user_habits": profile.user_habits,
                "profile_photo_url": photo_url,
            }
            return profile_dict
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to update profile: {str(e)}"
            )

    async def create_profile(
        self, session: AsyncSession, email: str, profile_data: dict
    ):

        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=400, detail="Not such user")
        profile_data["user_id"] = user.id
        stmt = insert(self.model).values(**profile_data).returning(self.model)
        result = await session.execute(stmt)
        profile = result.scalar_one_or_none()

        # await session.commit()
        # await session.refresh(profile)

        return profile

    async def set_user_profile_photo(
        self, user_id: int, data_dict: dict, session: AsyncSession
    ):
        stmt = select(self.model.id).where(self.model.user_id == user_id)
        try:
            result = await session.execute(stmt)
            profile_id = result.scalar_one_or_none()
            if profile_id is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Profile not found for user_id={user_id}"
                )
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
                # session.add(user_photo)
                # await session.commit()
                # await session.refresh(user_photo)

            return user_photo

        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to set photo: {str(e)}"
            )

    async def get_habits(self, session: AsyncSession):
        stmt = select(Habits.name)
        result = await session.execute(stmt)
        habits = result.scalars().all()
        return list(habits)
