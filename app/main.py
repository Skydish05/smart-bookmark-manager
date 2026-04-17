from fastapi import FastAPI
from app.routers.bookmarks import router
from app.database import engine, Base
from app.models.bookmark import Bookmark

Base.metadata.create_all(bind=engine)

app = FastAPI(title = "Smart Bookmark Manager")
app.include_router(router)

@app.get("/")
def root():
    return {"message" : "The app is running"}