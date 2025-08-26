from utils.location_repository import SQLAlchemyLocationRepository
from models.user import User


class LocationRepository(SQLAlchemyLocationRepository):
    model = User
