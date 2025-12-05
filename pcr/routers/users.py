from fastapi import APIRouter,HTTPException,Depends
from fastapi.security import OAuth2PasswordRequestForm
from pcr.models.users import User,UserResponse,Token,Message,Users
from pcr.repositories.user_repository import CRUDUsers
from http import HTTPStatus
from pcr.security import (
    hash,verify_password,create_access_token,get_current_user,verify_credentials
)
from typing import Annotated
from pcr.routers.dependencies import get_user_service
from pcr.services.user_service import UserService


app = APIRouter(tags=["users"],prefix="/users")

@app.get("/",response_model = Users)
async def get_users(user_service: UserService = Depends(get_user_service)):
    users = await user_service.get_users()
    return {"users":users}

@app.post("/",response_model = UserResponse)
async def register_user(user:User,user_service: UserService = Depends(get_user_service)):
    user_id = await user_service.add_user(user)
    return {
        "id":user_id,
        "username":user.username,
        "email":user.email
    }

@app.post("/token",response_model = Token)
async def create_token(
    form_data : Annotated[OAuth2PasswordRequestForm,Depends()]
):
    token = create_access_token(form_data)
    return {
        "access_token":token,
        "token_type": "Bearer"
    }

@app.delete("/{id}",response_model = Message)
async def delete_user(id:int,authenticated_user = Depends(get_current_user)):
    if id != authenticated_user["id"]:
        raise HTTPException(
            status_code = HTTPStatus.UNAUTHORIZED,
            detail = "unauthorized request"
        )
    await manage_users.delete_user_from_table((id,))
    return {"Message": "User deleted!"}

@app.put("/{id}",response_model = Message)
async def update_user(
id:int,user:User,authenticated_user = Depends(get_current_user)
):
    if id != authenticated_user["id"]:
        raise HTTPException(
            status_code = HTTPStatus.UNAUTHORIZED,
            detail = "unauthorized request"
        )
    await verify_credentials(
        account.username,
        account.email
    )
    await manage_users.update_user_from_table(
        (
            account.username,
            account.email,
            account.password,
            id
        )
    )
    return {"Message":"updated user"}
    