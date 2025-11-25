import os 
from mysql.connector.aio import connect
from dotenv import load_dotenv


load_dotenv()

class MysqlConnection:

    def __init__(self):
        self._host = os.getenv('HOST')
        self._user = os.getenv('USER')
        self._password = os.getenv('PASSWORD')
        self._database = os.getenv('DATABASE')
        self.conn = None

    async def _connection(self):
        return await connect(
            user = self.db._user,
            password = self.db._password,
            host = self.db._host,
            database = self.db._database
        )
    
    async def _query(self,query:str,data=None) -> list:
        if not self.db.conn:
            self.db.conn = await self._connection()
        async with await self.db.conn.cursor(dictionary=True) as cursor:
            await cursor.execute(query,data)
            response = await cursor.fetchall()
            if data:
                await self.db.conn.commit()
            return response



    

