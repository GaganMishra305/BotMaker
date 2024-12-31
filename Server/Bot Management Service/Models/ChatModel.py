from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict
from datetime import datetime
from uuid import UUID, uuid4


class Chat(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    bot_id: UUID
    messages: List[str] = Field(default_factory=list)

    def to_db(self) -> dict:
        return {
            "id": str(self.id),
            "bot_id": str(self.bot_id),
            "messages": self.messages
        }