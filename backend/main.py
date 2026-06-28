from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.sentiment_routes import router
from backend.database.database import Base, engine

app = FastAPI(
    title="Amazon Sentiment API"
)

from fastapi.middleware.cors import CORSMiddleware

# ... (your other code)

app.add_middleware(
    CORSMiddleware,
    # Using a wildcard allows Vercel to bypass preflight locks entirely
    allow_origins=["*"], 
    allow_credentials=False,  # Must be False if allow_origins is "*"
    allow_methods=["*"],      # Allows POST, OPTIONS, GET, etc.
    allow_headers=["*"],      # Allows Content-Type, Authorization, etc.
)

Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "API Running"
    }