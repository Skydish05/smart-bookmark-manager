from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.bookmark import BookmarkCreate, BookmarkUpdate
from app.models.bookmark import Bookmark
from app.dependencies import get_db
from app.services.scraper import scrape_metadata


router = APIRouter()

@router.post("/bookmarks")
async def create_bookmark(bookmark: BookmarkCreate, db: Session = Depends(get_db)):
    if not bookmark.url.startswith("http"):
        bookmark.url = "https://" + bookmark.url
    new_bookmark = Bookmark(url = bookmark.url, tags = bookmark.tags)
    db.add(new_bookmark)
    db.commit()
    db.refresh(new_bookmark)
    metadata = await scrape_metadata(bookmark.url)
    new_bookmark.title = metadata["title"]
    new_bookmark.description = metadata["description"]
    db.commit()
    db.refresh(new_bookmark)
    return new_bookmark

@router.get("/bookmarks")
def list_bookmarks(db: Session = Depends(get_db)):
    return db.query(Bookmark).all()

@router.get("/bookmarks/{bookmark_id}")
def get_bookmark(bookmark_id: int, db: Session = Depends(get_db)):
    bookmark = db.query(Bookmark).filter(Bookmark.id == bookmark_id).first()
    if not bookmark:
        raise HTTPException(status_code = 404, detail = "Bookmark not found")
    return bookmark

@router.put("/bookmarks/{bookmark_id}")
def update_bookmark(bookmark_id: int, updates: BookmarkUpdate, db: Session = Depends(get_db)):
    bookmark = db.query(Bookmark).filter(Bookmark.id == bookmark_id).first()
    if not bookmark:
        raise HTTPException(status_code = 404, detail = "Bookmark not found")
    if updates.title is not None:
        bookmark.title = updates.title
    if updates.tags is not None:
        bookmark.tags = updates.tags
    db.commit()
    db.refresh(bookmark)
    return bookmark

@router.delete("/bookmarks/{bookmark_id}", status_code=204)
def delete_bookmark(bookmark_id: int, db: Session = Depends(get_db)):
    bookmark = db.query(Bookmark).filter(Bookmark.id == bookmark_id).first()
    if not bookmark:
        raise HTTPException(status_code = 404, detail = "Bookmark not found")
    db.delete(bookmark)
    db.commit()