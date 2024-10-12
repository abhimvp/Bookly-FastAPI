# All our models will be located in this file

import uuid
from typing import List,Optional
from datetime import datetime,date
from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg


# User Authentication model
class User(SQLModel, table=True):
    __tablename__ = "users" # type: ignore
    uid: uuid.UUID = Field(  # to access uuid type for postgreSQL
        sa_column=Column(
            pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4
        )  # to generate uuid for each row
    )  # defining it as SQLAlchemy field
    username: str
    password_hash: str = Field(exclude=True)
    email: str
    firstname: str
    lastname: str
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Book(SQLModel, table=True):
    __tablename__ = "books"  # type: ignore

    uid: uuid.UUID = Field(  # to access uuid type for postgreSQL
        sa_column=Column(
            pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4
        )  # to generate uuid for each row
    )  # defining it as SQLAlchemy field
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default=None,foreign_key="users.uid")  # going to be an optional field because it's going to be a nullable field anyway
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    user: Optional["User"] = Relationship(back_populates="books")

    def __repr__(self) -> str:
        return f"<Book {self.title}>"
