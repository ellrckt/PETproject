from abc import ABC, abstractmethod
from sqlalchemy import select, insert, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from models.user import User
from models.location import UserLocation
from schemas.user.user import UserCityCountry


class AbstractLocationRepository(ABC):

    @abstractmethod
    async def set_user_location(self):
        raise NotImplementedError


class SQLAlchemyLocationRepository(AbstractLocationRepository):

    model = User

    async def set_user_location(
        self, location: dict, session: AsyncSession, email: str, city: str, country: str
    ) -> UserCityCountry:
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
                user_id=user_id,
                geom=func.ST_MakePoint(location["lng"], location["lat"]),
                city=city,
                country=country,
            )
            result = await session.execute(stmt)
            await session.commit()
            return UserCityCountry(city=city, country=country)

    async def set_user_lat_lng(
        self, 
        location: dict, 
        session: AsyncSession, 
        email: str, 
        city: str, 
        country: str
    ) -> UserCityCountry:
        
        result = await self.set_user_location(location, session, email, city, country)

        return result