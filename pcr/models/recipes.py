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

