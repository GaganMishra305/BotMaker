from pydantic import BaseModel, EmailStr, Field

class UserRequestModel(BaseModel):
    username: str
    username: str
    email: EmailStr
    password: str