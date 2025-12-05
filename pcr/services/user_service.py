from pcr.repositories.user_repository import UserRepository
from pcr.security import verify_credentials
from pcr.security import hash
from pcr.models.users import User


class UserService:

    def __init__(self,user_repository:UserRepository):
        self.user_repository = user_repository
    
    async def get_users(self) -> dict:
        users = await self.user_repository.get_users()
        return users

    async def add_user(self,user:User):
        await verify_credentials(
            user.username,
            user.email
        )
        user_id = await self.user_repository.add_user(
            user.username,
            user.email,
            hash(user.password)
        )
        return user_id
        