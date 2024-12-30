from fastapi import APIRouter, Depends
from Db.get_db import get_db

chat_router = APIRouter()