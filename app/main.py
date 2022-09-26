import imp
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body

from pydantic import BaseModel
from typing import Optional
from random import randrange

import psycopg2
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None






my_posts = {1: {'title': 'top beaches in florida',
                'content': 'check out2210...'}}


@app.get("/")
async def root():
    return {"message": "Welcome to API 2"}


@app.get("/posts")
def get_posts():
    return {"data:": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(payLoad: Post):
    post_dict = payLoad.dict()
    ID = randrange(0, 1000)
    print(ID)
    my_posts[ID] = post_dict
    print(my_posts)
    return {"data received": ID}


def find_post(id):
    if id in my_posts:
        return my_posts[id]


@app.get("/posts/latest")
def get_latest_post():
    return {"post_details": my_posts[-1]}

# conver id to string as it is auto converted to str
@app.get("/posts/{id}")
def get_post(id: str):
    post = find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_details": f"{post}"}


@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int):
    if id in my_posts:
        del my_posts[id]
        print("deleted", my_posts)

        return Response(status_code=204)

    else:
        raise HTTPException(
            status_code=404, detail=f"post with id: {id} was not found")


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    if id in my_posts:
        my_posts[id] = post.dict()
        return {"Updated"}
    else:
        raise HTTPException(
            status_code=404, detail=f"post with id: {id} was not found")

    