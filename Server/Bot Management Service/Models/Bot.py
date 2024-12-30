from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict
from datetime import datetime
from uuid import UUID, uuid4

class Bot(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    creator_id: UUID
    config: Dict = Field(default_factory=dict)  # Simple configuration storage
    
    def to_db(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "creator_id": str(self.creator_id),
            "config": self.config
        }

