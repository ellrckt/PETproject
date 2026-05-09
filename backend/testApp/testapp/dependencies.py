from repository.user import UserRepository, SQLAlchemyUserCRUDRepository
from repository.auth import AuthRepository
from repository.profile import ProfileRepository
# from repository.location import LocationRepository
from repository.subscription import SubscriptionRepository

# from services.location import LocationService
from services.user import UserService, UserCRUDService
from services.auth import AuthService
from services.profile import ProfileService
from services.subscription import SubscriptionService

from translate_manager.translate_manager import TranslatorManager
from redis_service.redis_profile_service import RedisJSONProfileService
from redis_service.redis_chat_service import RedisChatManager

def subscription_service():
    return SubscriptionService(SubscriptionRepository)


def redis_json_service() -> RedisJSONProfileService:
    return RedisJSONProfileService()


# def location_service():
#     return LocationService(LocationRepository)


def profile_service():
    return ProfileService(ProfileRepository)


def user_service():
    return UserService(UserRepository)


def auth_service():
    return AuthService(AuthRepository)


def user_crud_service():
    return UserCRUDService(SQLAlchemyUserCRUDRepository)

def get_ws_service():
    from chats.chat_service import WebSocketManager
    return WebSocketManager()

def get_redis_chat_service():
    return RedisChatManager()

def get_translate_manager():
    return TranslatorManager()

    