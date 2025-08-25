from fastapi import Request
from geopy.geocoders import Nominatim
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import decode_jwt
from utils.location_repository import AbstractLocationRepository


class LocationService:

    def __init__(self, location_repository: AbstractLocationRepository):

        self.location_repository = location_repository()

    async def get_city_country(self, location: dict):

        latitude = location["lat"]
        longitude = location["lng"]
        geolocator = Nominatim(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 OPR/120.0.0.0"
        )
        location = geolocator.reverse(
            f"{latitude}, {longitude}", exactly_one=True, language="en"
        )

        if location:
            address = location.raw.get("address", {})
            country = address.get("country", "")
            city = (
                address.get("city", "")
                or address.get("town", "")
                or address.get("village", "")
            )
            return city, country
        return None, None

    async def set_user_lat_lng(
        self, schema: dict, session: AsyncSession, request: Request
    ):
        
        location = schema.model_dump()
        refresh_token = request.cookies.get("refresh_token")
        payload = decode_jwt(refresh_token)
        email = payload["email"]

        city, country = await self.get_city_country(location)
        result = await self.location_repository.set_user_lat_lng(
            location, session, email, city, country
        )
        return result
