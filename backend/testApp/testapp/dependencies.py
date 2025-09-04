from repository.user import UserRepository, SQLAlchemyUserCRUDRepository
from repository.auth import AuthRepository
from repository.profile import ProfileRepository
from repository.location import LocationRepository


from services.location import LocationService
from services.user import UserService, UserCRUDService
from services.auth import AuthService
from services.profile import ProfileService

from redis_service.redis_profile_service import RedisJSONProfileService

def redis_json_service()->RedisJSONProfileService:
    return RedisJSONProfileService()

def location_service():
    return LocationService(LocationRepository)

def profile_service():
    return ProfileService(ProfileRepository)


def user_service():
    return UserService(UserRepository)


def auth_service():
    return AuthService(AuthRepository)


def user_crud_service():
    return UserCRUDService(SQLAlchemyUserCRUDRepository)
