from pcr.database import MysqlConnection


class UserRepository:

    def __init__(self):
        self.connection = MysqlConnection()

    async def get_users(self) -> dict:
        users = await self.connection._query("""
            SELECT id,
                username,
                email
            FROM user
            LIMIT 20;
            """
        )
        return users
            
    async def get_conflict_user(
        self,username:str = '',email:str = ''
    ) -> dict:
        users = await self.connection._query("""
            SELECT id,
                username,
                email,
                password
            FROM user
            WHERE username = (%s) or
            email = (%s)
            LIMIT 1;
            """,(username,email)
        )
        for user in users:
            return user
    
    async def add_user(self,data:tuple) -> None:
        await self.connection._query("""
            INSERT INTO user(
                username,
                email,
                password
            )
            VALUES (%s,%s,%s);
            """,data
        )
    
    async def delete_user(self,data:tuple) -> None:
        await self.connection._query("""
            DELETE FROM user WHERE ID = %s;
            """,data
        )
    
    async def update_user(self,data:tuple):
        await self.connection._query("""
            UPDATE user  SET
                username = %s,
                email = %s,
                password = %s
            WHERE id = %s;
        """,data
        )
    