from pcr.repositories.user_repository import UserRepository


class UserService:

    def __init__(self,user_repository:UserRepository):
        self.user_repository = user_repository
    
    async def get_users(self) -> dict:
        users = await self.user_repository.get_users()
        return users
        