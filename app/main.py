from fastapi import FastAPI
from app.routers.bookmarks import router as bookmarks_router
from app.routers.auth import router as auth_router
from app.database import engine, Base
from app.models.bookmark import Bookmark
from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI(title = "Smart Bookmark Manager")
app.include_router(bookmarks_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message" : "The app is running"}