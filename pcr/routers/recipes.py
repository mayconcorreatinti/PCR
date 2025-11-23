from fastapi import APIRouter,Body,Depends
from pcr.models.recipes import Recipe
from pcr.database import CRUDRecipes,CRUDIngredients,CRUDInstructions
from pcr.security import get_current_user
import json


app = APIRouter(tags=["recipes"],prefix="/recipes")
manage_recipes = CRUDRecipes()
manage_ingredients = CRUDIngredients()
manage_instructions = CRUDInstructions()

@app.get("/")
def get_recipes():
    with open("pcr/recipes.json","r",encoding='utf8') as file:
        return json.load(file)

@app.post("/")
async def post_recipe(recipe: Recipe,authenticated_user = Depends(get_current_user)):
    await manage_recipes.insert_recipe_into_table(
        authenticated_user["id"],
        recipe.name,
        recipe.description,
        recipe.prep_time,
        recipe.serve,
    )

    