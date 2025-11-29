from pcr.database import MysqlConnection


class UserService:

    def __init__(self):
        self.connection = MysqlConnection()

    async def select_users_from_table(self) -> dict:
        users = await self.connection._query("""
            SELECT id,
                username,
                email
            FROM user
            LIMIT 20;
            """
        )
        return users
            
    async def select_user_from_table(
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
    
    async def insert_user_into_table(self,data:tuple) -> None:
        await self.connection._query("""
            INSERT INTO user(
                username,
                email,
                password
            )
            VALUES (%s,%s,%s);
            """,data
        )
    
    async def delete_user_from_table(self,data:tuple) -> None:
        await self.connection._query("""
            DELETE FROM user WHERE ID = %s;
            """,data
        )
    
    async def update_user_from_table(self,data:tuple):
        await self.connection._query("""
            UPDATE user  SET
                username = %s,
                email = %s,
                password = %s
            WHERE id = %s;
        """,data
        )
    