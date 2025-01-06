from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict
from datetime import datetime
from uuid import UUID, uuid4


class Message(BaseModel):
    role : str
    content : str
    
    def to_db(self):
        return {
            "role" : self.role, 
            "content" : self.content
        }

class Chat(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    bot_id: UUID
    messages: List[Message] = Field(default_factory=list)
