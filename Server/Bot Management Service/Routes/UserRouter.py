from fastapi import APIRouter, Depends
from Db.get_db import get_db

user_router = APIRouter()

@user_router.get("/")
def get_users(db=Depends(get_db)):
    collections = db.list_collection_names()
    return {"message": "List of users", "collections": collections}

@user_router.get("/{user_id}")
def get_user(user_id: int, db=Depends(get_db)):
    return {"message": f"Details of user {user_id}"}
