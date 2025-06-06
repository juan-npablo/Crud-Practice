from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    user_id: Optional[int]
    email: EmailStr
    name: str
    password: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None

