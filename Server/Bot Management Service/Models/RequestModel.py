from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRequestModel(BaseModel):
    username: str
    username: str
    email: EmailStr
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    
    def get_password_hash(password):
        return pwd_context.hash(password)
    
    def to_db(self) -> dict:
        return {
            "username": self.username,
            "email": self.email,
            "password": pwd_context.hash(self.password), 
            "created_at": self.created_at.isoformat()
        }
        
class TokenData(BaseModel):
    username: str | None = None
    
class Token(BaseModel):
    access_token: str
    token_type: str
