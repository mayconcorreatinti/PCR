from fastapi import APIRouter,Depends,HTTPException
from pcr.models.recipes import Recipe,RecipeResponse
from pcr.repositories.recipe_repository import (
  CRUDRecipes,CRUDIngredients,CRUDInstructions
)
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

@app.post("/",status_code=HTTPStatus.CREATED,response_model=RecipeResponse)
async def post_recipe(recipe: Recipe,authenticated_user = Depends(get_current_user)):
    recipe_db = await manage_recipes.select_recipe_from_table(
        ("description",recipe.description)
      )
    if recipe_db:
      raise HTTPException(
        status_code=HTTPStatus.CONFLICT,
        detail="This recipe description already exists!"
      )
    await manage_recipes.insert_recipe_into_table(
      (
        authenticated_user["id"],
        recipe.name,
        recipe.description,
        recipe.prep_time,
        recipe.serve,
      )
    )
    recipe_db = await manage_recipes.select_recipe_from_table(
        ("description",recipe.description)
      )
    for ingredient in recipe.ingredients:
      await manage_ingredients.insert_ingredient_into_table(
        (
          recipe_db["id"],
          ingredient.name,
          ingredient.quantity
        )
      )
    for instruction in recipe.instructions:
      await manage_instructions.insert_instruction_into_table(
        (
          recipe_db["id"],
          instruction.step_number,
          instruction.description
        )
      )
    return {
      "id": recipe_db["id"],
      "user_id": authenticated_user["id"],
      "name": recipe.name,
      "description": recipe.description,
      "ingredients": recipe.get_ingredients(),
      "instructions": recipe.get_instructions(),
      "prep_time": recipe.prep_time,
      "serve": recipe.serve
    }