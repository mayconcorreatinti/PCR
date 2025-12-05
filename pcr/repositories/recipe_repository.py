from pcr.database import MysqlConnection
from pcr.models.recipes import Ingredient,Instruction


class RecipeRepository:

    def __init__(self):
        self.connection = MysqlConnection()
    
    async def add_recipe(self,data:tuple):
        recipe_id = await self.connection._query("""
            INSERT INTO recipe(
                user_id,
                name,
                description,
                prep_time,serves
            ) VALUES (%s,%s,%s,%s,%s);
            SELECT LAST_INSERT_ID();              
        """,data
        )
        return recipe_id

    async def add_ingredient(self,recipeid,ingredients:list[Ingredient]) -> None:
        for ingredient in ingredients:
            await self.connection._query("""
                INSERT INTO ingredient(
                    recipe_id,
                    name,
                    quantity
                ) VALUES (%s,%s,%s);
            """,(
                    recipeid,
                    ingredient.name,
                    ingredient.quantity
                )
            )

    async def add_instruction(self,recipeid,instructions:list[Instruction]) ->None:
        for instruction in instructions:
            await self.connection._query("""
                INSERT INTO Instruction(
                    recipe_id,
                    step_number,
                    description
                ) VALUES (%s,%s,%s);
            """,(
                    recipeid,
                    instruction.step_number,
                    instruction.description
                )
            )
         