from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=['posts'])


@router.get("/all", response_model=List[schemas.PostVoteResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id ==
                                                                                       models.Post.id, isouter=True).group_by(models.Post.id).all()
    return posts


@router.get("/", response_model=List[schemas.PostVoteResponse])
def get_posts(db: Session = Depends(get_db), limit: int = 3, skip: int = 0, search: Optional[str] = '', current_user: int = Depends(oauth2.get_current_user)):
    # access via posts?limit=4&skip=0&search=HOUSES %20 IS SPACE
    # use skip to show results on different pages

    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id ==
                                                                                         models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(payLoad: schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id, **payLoad.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=404, detail=f"post with id: {id} not found!")
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail=f"Not authorised")
    return post


@router.delete("/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(
            status_code=404, detail=f"post with id: {id} was not found")
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=403)
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)


@router.put("/{id}")
def update_post(id: int, post: schemas.UpdatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    updatePost = db.query(models.Post).filter(models.Post.id == id)
    postF = updatePost.first()
    if postF and postF.owner_id == current_user.id:
        updatePost.update(post.dict(), synchronize_session=False)
        db.commit()
        return updatePost.first()
    if postF.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail=f"User do not have permission")
    if not postF:
        raise HTTPException(
            status_code=404, detail=f"post with id: {id} was not found")
