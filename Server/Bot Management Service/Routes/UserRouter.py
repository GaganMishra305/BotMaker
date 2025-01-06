from datetime import timedelta
import os
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from Db.get_db import get_db
from Models.RequestModel import Token, UserRequestModel
from Models.UserModel import User
from Controllers.UserController import authenticate_user, create_access_token, get_all_users_fn, get_current_active_user, get_user_by_id_or_username_fn, create_user_fn
from dotenv import load_dotenv

load_dotenv('.env')

user_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 1. Create
@user_router.post('/')
async def create_user(user: UserRequestModel, db = Depends(get_db)):
    user = await create_user_fn(user, db)
    
    if user:
        return user
    else:
        raise HTTPException(status_code=403, detail="Failed to create user.")

# 2. Read
@user_router.get("/")
async def get_all_users(db = Depends(get_db)):
    users = await get_all_users_fn(db)
    return users

@user_router.get("/id")
async def get_user_by_id_or_username(id: str, db=Depends(get_db)):
    user = await get_user_by_id_or_username_fn(id, db)
    
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@user_router.get("/username")
async def get_user_by_id_or_username(uname: str, db=Depends(get_db)):
    user = await get_user_by_id_or_username_fn(uname, db)
    
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
    
# TODO : debug this and make it usable
# 3. Update
# @user_router.put("/id")
# async def update_user_by_id_or_username(id: str, user: UserRequestModel, db=Depends(get_db)):
#     user_collection = db.users
#     user = await get_user_by_id_or_username_fn(id, db)
    
#     if user:
#         user_collection.update_one({"_id" : id}, {"$set" : user})
#         return {"Updated user" : user}
#     else:
#         raise HTTPException(status_code=404, detail="User not found")
    
# 4. Delete
@user_router.delete("/id")
async def delete_user_by_id(id: str, db=Depends(get_db)):
    user_collection = db.users
    user = await get_user_by_id_or_username_fn(id, db)
    
    if user:
        user_collection.delete_one({"_id" : id})
        return {"Deleted user" : user}
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
# 5. Auth
@user_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db = Depends(get_db),
) -> Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@user_router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user