from pydantic import BaseModel,Field
from typing import List


class Ingredient(BaseModel):
    name: str
    quantity: str

class Instruction(BaseModel):
    step_number: int
    description: str

class Recipe(BaseModel):
    name: str
    description: str
    ingredients: List[Ingredient] = Field(
        example = [
            {
                "name": "string",
                "quantity": "string"
            },
            {
                "name": "string",
                "quantity": "string"
            }
        ]
    )
    instructions: List[Instruction] = Field(
        example = [
            {
                "step_number": 1,
                "description": "string"
            },
            {
                "step_number": 2,
                "description": "string"
            }
        ]
    )
    prep_time: str
    serve: str | None

    def get_ingredients(self):
        dict_ingredients = []
        for ingredient in self.ingredients:
            dict_ingredients.append(dict(ingredient))
        return dict_ingredients

    def get_instructions(self):
        dict_instructions = []
        for instruction in self.instructions:
            dict_instructions.append(dict(instruction))
        return dict_instructions

class RecipeResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: str
    ingredients: List[Ingredient]
    instructions: List[Instruction]
    prep_time: str
    serve: str | None

class Recipes(BaseModel):
    recipes: List[RecipeResponse]