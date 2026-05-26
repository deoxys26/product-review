from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.sentiment_routes import router
from backend.database.database import Base, engine

app = FastAPI(
    title="Amazon Sentiment API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "API Running"
    }