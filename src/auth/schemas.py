import uuid
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field
from src.books.schemas import Book

class UserCreateModel(BaseModel):
    firstname: str = Field(min_length=3, max_length=28)
    lastname: str = Field(min_length=3, max_length=28)
    username: str = Field(min_length=3, max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6, max_length=16)


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    password_hash: str
    email: str
    firstname: str
    lastname: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    books: List[Book]


class UserLoginModel(BaseModel):
    password: str
    email: str
