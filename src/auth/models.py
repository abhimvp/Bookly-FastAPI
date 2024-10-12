# User Authentication model
import uuid
from typing import List
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from src.books import models


class User(SQLModel, table=True):
    __tablename__ = "users"
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
    books: List["models.Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self) -> str:
        return f"<User {self.username}>"
