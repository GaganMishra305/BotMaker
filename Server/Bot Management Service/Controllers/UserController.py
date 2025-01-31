from datetime import datetime, timedelta, timezone
import os
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
import jwt
from streamlit import status
from Models.RequestModel import TokenData, UserRequestModel
from Models.UserModel import User
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv('.env')
# 1. crud
async def get_all_users_fn(db):
    user_collection = db.users
    users = user_collection.find()
    return list(users)

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
    saved_user = user_collection.insert_one(user.to_db())
    
    # 3. Check if saved or not
    return saved_user


# 2. Auth
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = "HS256"

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

async def authenticate_user(db, username: str, password: str):
    user = await get_user_by_id_or_username_fn( username, db)
    if not user:
        return False
    if not verify_password(password, user['password']):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = await get_user_by_id_or_username_fn(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user