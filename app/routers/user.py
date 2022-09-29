from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session

import sys
sys.path.append("..")
from utils import hash_password
import models, schemas
from database import get_db

router = APIRouter(prefix="/users", tags=['users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
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


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    u = db.query(models.User).filter(models.User.id == id).first()
    if not u:
        raise HTTPException(
            status_code=404, detail=f"user with id: {id} was not found")
    return u
