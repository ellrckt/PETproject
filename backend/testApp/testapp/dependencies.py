from repository.user import UserRepository
from services.user import UserService


def user_service():
    return UserService(UserRepository)
