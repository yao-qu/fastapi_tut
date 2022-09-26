from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body

from pydantic import BaseModel
from typing import Optional
from random import randrange
import time
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

host = 'localhost'
database ='fastAPI'
user = 'postgres'
password = 'bear'
while True:
    try:
        conn = psycopg2.connect(host = host, database=database, user=user, password=password, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connected!")
        break
    except Exception as error:
        print("Connection failed", error)
        time.sleep(5)


my_posts = {1: {'title': 'top beaches in florida',
                'content': 'check out2210...'}}


@app.get("/")
async def root():
    return {"message": "Welcome to API 2"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data:": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(payLoad: Post):
    # DO NOT USE FORMAT STRING, SECURITY ISSUE
    # USE %S TO SANITISE THE STATEMENTS
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING * """, (payLoad.title, payLoad.content, payLoad.published))
    new_post = cursor.fetchone()
    # NEED TO COMMIT
    conn.commit()
    return {"Post created": new_post}

def find_post(id):
    if id in my_posts:
        return my_posts[id]


@app.get("/posts/latest")
def get_latest_post():
    return {"post_details": my_posts[-1]}

# conver id to string as it is auto converted to str
@app.get("/posts/{id}")
def get_post(id: str):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail=f"post with id: {id} not found!")
    return {"post detail": post}


@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    post = cursor.fetchone()
    conn.commit()
    if post:
        return Response(status_code=204)

    else:
        raise HTTPException(
            status_code=404, detail=f"post with id: {id} was not found")


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))

    updatePost = cursor.fetchone()
    conn.commit()
    if updatePost:
        return {"Updated": updatePost}
    else:
        raise HTTPException(
            status_code=404, detail=f"post with id: {id} was not found")

    