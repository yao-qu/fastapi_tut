from fastapi import FastAPI, Response, status, HTTPException, Depends
import models
from database import engine
from routers import post, user, auth
from config import settings
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to API 2"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
