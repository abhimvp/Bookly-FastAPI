import uuid
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field
from src.books.schemas import Book
from src.reviews.schemas import ReviewModel

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
    
class UserWithBookModel(UserModel):
    books: List[Book]
    reviews: List[ReviewModel]


class UserLoginModel(BaseModel):
    password: str
    email: str

class EmailModel(BaseModel):
    addresses : List[str]
    
... #the rest of the code
class PasswordResetRequestModel(BaseModel):
    email: str


class PasswordResetConfirmModel(BaseModel):
    new_password: str
    confirm_new_password: str