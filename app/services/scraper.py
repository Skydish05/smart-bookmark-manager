import httpx
from bs4 import BeautifulSoup

async def scrape_metadata (url: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout = 10)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else None
        meta_desc = soup.find("meta", attrs={"name", "description"})
        if not meta_desc:
            meta_desc = soup.find("meta", attrs={"property": "og:description"})
        description = meta_desc["content"] if meta_desc else None
        return {"title": title, "description": description}
    except Exception:
        return {"title": None, "description": "Invalid url"}