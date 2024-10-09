# User Authentication model
import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg


class User(SQLModel,table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field( # to access uuid type for postgreSQL
     sa_column= Column(
         pg.UUID,
         nullable=False,
         primary_key=True,
         default=uuid.uuid4
      ) # to generate uuid for each row
     ) #defining it as SQLAlchemy field
    username: str
    password_hash: str = Field(exclude=True)
    email: str
    firstname: str
    lastname: str
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at: datetime= Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))

    def __repr__(self) -> str:
       return f"<User {self.username}>"
    