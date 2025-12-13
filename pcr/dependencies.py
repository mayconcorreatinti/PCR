from pcr.services.user_service import UserService,UserSecurityService
from pcr.repositories.user_repository import UserRepository


def get_user_service():
    return UserService(UserRepository)

def get_user_Security_service():
    return UserSecurityService(UserRepository)