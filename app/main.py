from fastapi.middleware.cors import CORSMiddleware
from routers import post, user, auth, vote
from database import engine
import models
from fastapi import FastAPI, Response, status, HTTPException, Depends
import sys
sys.path.append("..")

from config import settings
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ['*']
# fetch(‘http://localhost:8000/').then(res => res.json()).then(console.log)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to API 2"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
