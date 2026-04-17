from pydantic import BaseModel

class BookmarkCreate(BaseModel):
    url: str
    tags: list[str] = []

class BookmarkUpdate(BaseModel):
    title: str | None = None
    tags: list[str] | None = None