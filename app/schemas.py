# pydantic model defines the structure of the request and response
# model is the table structure of the DB
from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class UpdatePost(BaseModel):
    title: str
    content: str
    published: bool


class PostResponse(UpdatePost):

    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    # created_at: datetime


class UserResponse(BaseModel):
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
