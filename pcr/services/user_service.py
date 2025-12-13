from pcr.repositories.user_repository import UserRepository
from pcr.models.users import User
from fastapi import HTTPException
from http import HTTPStatus
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash 
import os
import jwt


class UserSecurityService:

    def __init__(self,user_repository:UserRepository):
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")
        self.password_hash = PasswordHash.recommended()
        self.user_repository = user_repository

    def hash(self,password: str) -> str:
        return self.password_hash.hash(password)

    def verify_password(self,password, hash) -> bool:
        return self.password_hash.verify(password, hash)

    async def check_authentication(self,form_data:OAuth2PasswordRequestForm,):
        user = await self.user_repository.get_conflict_user(email=form_data.username)
        if not user or not self.verify_password(form_data.password,user["password"]):
            raise HTTPException(
                detail = "Incorrect username or password!",
                status_code = HTTPStatus.FORBIDDEN
            )
        
    def check_authorization(id,authenticated_user_id):
        if id != authenticated_user_id:
            raise HTTPException(
                status_code = HTTPStatus.UNAUTHORIZED,
                detail = "unauthorized request"
            )

    async def get_current_user(self):
        token = self.oauth2_scheme
        credentials_exception = HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload:dict = jwt.decode(
                token,
                os.getenv("SECRET_KEY"),
                algorithms=[os.getenv("ALGORITHM")])
            email = payload.get("sub")
            if email is None:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception
        user = await self.user_repository.get_conflict_user(email=email)
        if user is None:
            raise credentials_exception
        return user

    async def create_access_token(self,form_data:OAuth2PasswordRequestForm):
        await self.check_authentication(form_data)
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

    async def verify_credentials(self,username:str,email:str):
        user = await self.user_repository.get_conflict_user(username,email)
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

class UserService:

    def __init__(self,user_repository:UserRepository):
        self.user_repository = user_repository
        self.security_service = UserSecurityService(user_repository)

    async def get_users(self) -> dict:
        users = await self.user_repository.get_users()
        return users

    async def add_user(self,user:User):
        await self.security_service.verify_credentials(
            user.username,
            user.email
        )
        user_id = await self.user_repository.add_user(
            user.username,
            user.email,
            hash(user.password)
        )
        return user_id
    
    async def get_user(self,email):
        user = await self.user_repository.get_conflict_user(email=email)
        return user

    async def delete_user(self,id,authenticated_user_id):
        self.security_service.check_authorization(
            id,
            authenticated_user_id
        )
        await self.user_repository.delete_user((id,))
    
    async def update_user(self,id,authenticated_user_id,user:User):
        self.security_service.check_authorization(
            id,
            authenticated_user_id
        )
        await self.security_service.verify_credentials(
            user.username,
            user.email
        )
        await self.user_repository.update_user(
            user.username,
            user.email,
            self.security_service.hash(user.password),
            id
        )
    
    

            