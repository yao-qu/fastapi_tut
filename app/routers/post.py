from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import os
import sys
sys.path.append("..")
from database import get_db
import models, schemas, oauth2
from typing import List
router = APIRouter(prefix="/posts", tags=['posts'])


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_posts(payLoad: schemas.CreatePost, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)
    new_post = models.Post(**payLoad.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=404, detail=f"post with id: {id} not found!")
    return post


@router.delete("/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first():
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=204)

    else:
        raise HTTPException(
            status_code=404, detail=f"post with id: {id} was not found")


@router.put("/{id}")
def update_post(id: int, post: schemas.UpdatePost, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    updatePost = db.query(models.Post).filter(models.Post.id == id)
    postF = updatePost.first()
    if postF:
        updatePost.update(post.dict(), synchronize_session=False)
        db.commit()
        return updatePost.first()
    else:
        raise HTTPException(
            status_code=404, detail=f"post with id: {id} was not found")
