from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict
from datetime import datetime
from uuid import UUID, uuid4
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    username: str
    email: EmailStr
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)
    
    def to_db(self) -> dict:
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "password": pwd_context.hash(self.password), 
            "created_at": self.created_at.isoformat()
        }