from pwdlib import PasswordHash 
from pcr.repositories.user_repository import CRUDUsers
from pcr.routers.dependencies import get_user_service
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import Depends,HTTPException
from http import HTTPStatus
from typing import Annotated
from jwt.exceptions import InvalidTokenError
import os
import jwt


password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")
manage_users = CRUDUsers()

def hash(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password, hash) -> bool:
    return password_hash.verify(password, hash)

async def verify_credentials(username:str,email:str):
    user = await manage_users.select_user_from_table(username,email)
    if user:
        if user["username"] == username:
            raise HTTPException(
                detail = "This name already exists!",
                status_code = HTTPStatus.CONFLICT
            )
        elif user["email"] == email:
            raise HTTPException(
                detail = "This email already exists!",
                status_code = HTTPStatus.CONFLICT
            )
        
async def check_authentication(
    form_data:OAuth2PasswordRequestForm,
    user_service = Depends(get_user_service)
):
    user = await user_service.get_user(email=form_data.username)
    if not user or not verify_password(form_data.password,user["password"]):
        raise HTTPException(
            detail = "Incorrect username or password!",
            status_code = HTTPStatus.FORBIDDEN
        )

async def create_access_token(form_data:OAuth2PasswordRequestForm):
    await check_authentication(form_data)
    to_encode = {"sub":form_data.username}
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        os.getenv("SECRET_KEY"),
        algorithm=os.getenv("ALGORITHM")
    )
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            os.getenv("SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await manage_users.select_user_from_table(email=email)
    if user is None:
        raise credentials_exception
    return user
