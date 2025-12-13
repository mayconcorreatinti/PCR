from fastapi import APIRouter,HTTPException,Depends
from fastapi.security import OAuth2PasswordRequestForm
from pcr.models.users import User,UserResponse,Token,Message,Users
from http import HTTPStatus
from typing import Annotated
from pcr.dependencies import get_user_service,get_user_Security_service
from pcr.services.user_service import UserService,UserSecurityService


app = APIRouter(tags=["users"],prefix="/users")

@app.get("/",response_model = Users)
async def get_users(
    user_service: UserService = Depends(get_user_service)
):
    users = await user_service.get_users()
    return {"users":users}

@app.post("/",response_model = UserResponse)
async def register_user(
    user:User,
    user_service: UserService = Depends(get_user_service)
):
    user_id = await user_service.add_user(user)
    return {
        "id":user_id,
        "username":user.username,
        "email":user.email
    }

@app.post("/token",response_model = Token)
async def create_token(
    form_data : Annotated[OAuth2PasswordRequestForm,Depends()],
    user_service: UserSecurityService = Depends(get_user_Security_service)
):
    token = user_service.create_access_token(form_data)
    return {
        "access_token":token,
        "token_type": "Bearer"
    }

@app.delete("/{id}",response_model = Message)
async def delete_user(
    id:int,
    authenticated_user = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    await user_service.delete_user(id,authenticated_user)
    return {"Message": "User deleted!"}

@app.put("/{id}",response_model = Message)
async def update_user(
    id:int,
    user:User,
    authenticated_user = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    await user_service.update_user(id,user,authenticated_user)
    return {"Message":"updated user"}
    