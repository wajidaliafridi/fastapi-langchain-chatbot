from pydantic import BaseModel, EmailStr
from typing import List, Optional


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserLogin):
    name: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str]


class User(UserCreate):
    id: int


