# pydantic model defines the structure of the request and response
# model is the table structure of the DB
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


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


class UserResponse(BaseModel):
    email: EmailStr
    created_at: datetime
    id: int

    class Config:
        orm_mode = True


class PostResponse(UpdatePost):
    id: int
    created_at: datetime
    owner_id: int
# return pydantic model UserResponse
    owner: UserResponse

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
