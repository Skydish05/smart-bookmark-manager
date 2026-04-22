A REST API where you save URLs and the backend automatically fetches page metadata (title, description). Built with FastAPI and PostgreSQL.

# Setup

1. Start the database:
docker compose up -d

2. Create a `.env` file:
DATABASE_URL=postgresql://bookmark_user:bookmark_pass@localhost:5433/bookmarks

3. Install dependencies:
pip install fastapi uvicorn sqlalchemy psycopg2-binary httpx beautifulsoup4 python-dotenv

4. Run the app:
uvicorn app.main:app --reload --port 8001

5. Open http://localhost:8001/docs to use the API

## Features 
- User registration and login with JWT authentication
- Save bookmarks (URL + optional tags)
- Auto-fetch page title and description
- AI-powered summaries using Groq
- Search across title, description, summary, and tags
- Each user only sees their own bookmarks