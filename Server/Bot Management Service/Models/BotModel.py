from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict
from datetime import datetime
from uuid import UUID, uuid4

class BotRequestModel(BaseModel):
    name: str
    creator_id: UUID
    model: str
    temperature:int
    prompt: str

    def to_db(self) -> dict:
        return {
            "name": self.name,
            "creator_id": str(self.creator_id),
            "model" : self.model,
            "temperature" : self.temperature,
            "prompt" : self.prompt
        }


class Bot(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    creator_id: UUID
    
    # config settings
    model: str
    temperature:int
    prompt: str
    
    
