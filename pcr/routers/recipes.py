from fastapi import APIRouter,Depends
from pcr.models.recipes import Recipe
from pcr.database import CRUDRecipes,CRUDIngredients,CRUDInstructions
from pcr.security import get_current_user
from http import HTTPStatus
import json


app = APIRouter(tags=["recipes"],prefix="/recipes")
manage_recipes = CRUDRecipes()
manage_ingredients = CRUDIngredients()
manage_instructions = CRUDInstructions()

@app.get("/")
def get_recipes():
    with open("pcr/recipes.json","r",encoding='utf8') as file:
        return json.load(file)

@app.post("/",status_code=HTTPStatus.CREATED)
async def post_recipe(recipe: Recipe,authenticated_user = Depends(get_current_user)):
    await manage_recipes.insert_recipe_into_table(
      (
        authenticated_user["id"],
        recipe.name,
        recipe.description,
        recipe.prep_time,
        recipe.serve,
      )
    )
    recipe_id = await manage_recipes.select_recipeid_from_table_by_description(
        (recipe.description,)
      )
    for ingredient in recipe.ingredients:
      await manage_ingredients.insert_ingredient_into_table(
        (
          recipe_id,
          ingredient.name,
          ingredient.quantity
        )
      )
    for instruction in recipe.instructions:
      await manage_instructions.insert_instruction_into_table(
        (
          recipe_id,
          instruction.step_number,
          instruction.description
        )
      )
    return "OK"