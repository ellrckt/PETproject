from repository.user import UserRepository,SQLAlchemyUserCRUDRepository
from services.user import UserService,UserCRUDService


def user_service():
    return UserService(UserRepository)

def user_crud_service():
    return UserCRUDService(SQLAlchemyUserCRUDRepository)
    