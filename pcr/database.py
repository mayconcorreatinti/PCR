import os 
from mysql.connector.aio import connect
from dotenv import load_dotenv


load_dotenv()

class Mysqldb:

    def __init__(self):
        self._host = os.getenv('HOST')
        self._user = os.getenv('USER')
        self._password = os.getenv('PASSWORD')
        self._database = os.getenv('DATABASE')
        self.conn = None


class ConnectionDB:

    def __init__(self):
        self.db = Mysqldb()

    async def _connection(self):
        return await connect(
            user = self.db._user,
            password = self.db._password,
            host = self.db._host,
            database = self.db._database
        )
    
    async def _query(self,query:str,data=None) -> list:
        if not self.conn:
            self.conn = await self._connection()
        async with await self.conn.cursor(dictionary=True) as cursor:
            await cursor.execute(query,data)
            response = await cursor.fetchall()
            if data:
                await self.conn.commit()
            return response


class CRUDUsers:

    def __init__(self):
        self.connection = ConnectionDB()

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
            INSERT INTO user(username,email,password)
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
    
class CRUDRecipes:

    def __init__(self):
        self.connection = ConnectionDB()
    
    async def insert_recipe_into_table(self,data:tuple) -> None:
        await self.connection._query("""
            INSERT INTO recipe(user_id,name,description ,prep_time,serves) VALUES (%s,%s,%s,%s,%s);
        """,data
        )


class CRUDIngredients:

    def __init__(self):
        self.connection = ConnectionDB()

    async def insert_ingredient_into_table(self,data:tuple) -> None:
        await self.connection._query("""
            INSERT INTO ingredient(recipe_id,name,quantity) VALUES (%s,%s,%s);
        """,data
        )


class CRUDInstructions:

    def __init__(self):
        self.connection = ConnectionDB()

    async def insert_instruction_into_table(self,data:tuple) ->None:
        await self.connection._query("""
            INSERT INTO Instruction(recipe_id,step_number,description) VALUES (%s,%s,%s);
        """,data
        )
         
