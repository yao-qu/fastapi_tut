# pydantic model defines the structure of the request and response
# model is the table structure of the DB
from pydantic import BaseModel


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
