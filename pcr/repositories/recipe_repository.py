from pcr.database import MysqlConnection


class CRUDRecipes:

    def __init__(self):
        self.connection = MysqlConnection()
    
    async def insert_recipe_into_table(self,data:tuple) -> None:
        await self.connection._query("""
            INSERT INTO recipe(
                user_id,
                name,
                description,
                prep_time,serves
            ) VALUES (%s,%s,%s,%s,%s);
        """,data
        )
    
    async def select_recipe_from_table(self,data):
        recipes = await self.connection._query("""
            SELECT id,
                user_id,
                name,
                description,
                prep_time,
                serves 
            FROM recipe 
            WHERE %s = %s;
        """,data
        )
        for recipe in recipes:
            return recipe

class CRUDIngredients:

    def __init__(self):
        self.connection = MysqlConnection()

    async def insert_ingredient_into_table(self,data:tuple) -> None:
        await self.connection._query("""
            INSERT INTO ingredient(
                recipe_id,
                name,
                quantity
            ) VALUES (%s,%s,%s);
        """,data
        )


class CRUDInstructions:

    def __init__(self):
        self.connection = MysqlConnection()

    async def insert_instruction_into_table(self,data:tuple) ->None:
        await self.connection._query("""
            INSERT INTO Instruction(
                recipe_id,
                step_number,
                description
            ) VALUES (%s,%s,%s);
        """,data
        )
         