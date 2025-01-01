from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from Models.RequestModel import UserRequestModel
from Models.UserModel import User

async def get_user_by_id_or_username_fn(id: str, db):
    user_collection = db.users    
    user = user_collection.find_one({"_id" : id})
    if user:
        return user
    
    user = user_collection.find_one({"username" : id})
    if user:
        return user
    
    raise HTTPException(status_code=404, detail="User not found")

async def create_user_fn(user: UserRequestModel, db):
    user_collection = db.users
    # 1. check for user with same username
    user_db = user_collection.find_one({"username" : user.username})
    if user_db is not None:
        raise HTTPException(status_code=400, detail="Username already exists") 
    
    # 2. try saving it in db
    saved_user = user_collection.insert_one(jsonable_encoder(user))
    
    # 3. Check if saved or not
    return saved_user