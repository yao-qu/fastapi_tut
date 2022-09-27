from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import models
from database import engine, get_db, SessionLocal
from sqlalchemy.orm import Session
import sys
import schemas
from typing import Optional, List
from utils import hash_password

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to API 2"}


@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_posts(payLoad: schemas.CreatePost, db: Session = Depends(get_db)):

    new_post = models.Post(**payLoad.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=404, detail=f"post with id: {id} not found!")
    return post


@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first():
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=204)

    else:
        raise HTTPException(
            status_code=404, detail=f"post with id: {id} was not found")


@app.put("/posts/{id}")
def update_post(id: int, post: schemas.UpdatePost, db: Session = Depends(get_db)):

    updatePost = db.query(models.Post).filter(models.Post.id == id)
    postF = updatePost.first()
    if postF:
        updatePost.update(post.dict(), synchronize_session=False)
        db.commit()
        return updatePost.first()
    else:
        raise HTTPException(
            status_code=404, detail=f"post with id: {id} was not found")


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_posts(payLoad: schemas.UserCreate, db: Session = Depends(get_db)):

    # HASH THE PASSWORD
    hashed_pwd = hash_password(payLoad.password)
    payLoad.password = hashed_pwd
    new_user = models.User(**payLoad.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    # {f"{new_user.email} created"}


@app.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    u = db.query(models.User).filter(models.User.id == id).first()
    if not u:
        raise HTTPException(
            status_code=404, detail=f"post with id: {id} was not found")
    return u
