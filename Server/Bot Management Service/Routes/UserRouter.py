from fastapi import APIRouter, Depends, HTTPException, Request
from Db.get_db import get_db
from Models.RequestModel import UserRequestModel
from Models.UserModel import User
from fastapi.encoders import jsonable_encoder
from Controllers.UserController import get_user_by_id_or_username_fn, create_user_fn

user_router = APIRouter()

@user_router.get("/{id_username}")
async def get_user_by_id_or_username(id: str, db=Depends(get_db)):
    user = await get_user_by_id_or_username(id, db)
    
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@user_router.post('/')
async def create_user(user: UserRequestModel, db = Depends(get_db)):
    user = await create_user_fn(user, db)
    
    if user:
        return user
    else:
        raise HTTPException(status_code=403, detail="Failed to create user.")
