from pcr.services.user_service import UserService
from pcr.repositories.user_repository import UserRepository


def get_user_service():
    return UserService(UserRepository)