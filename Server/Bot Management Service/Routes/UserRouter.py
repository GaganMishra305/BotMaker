from fastapi import APIRouter, Depends, Request
from Db.get_db import get_db
from Models.UserModel import User

user_router = APIRouter()

@user_router.get("/")
def get_users(db=Depends(get_db)):
    user_collection = db.users
    
    
@user_router.post('/')
def create_user(user: User, db = Depends(get_db)):
    user_collection = db.users
    return user
