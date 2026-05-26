from fastapi import APIRouter

from backend.schemas.sentiment_schema import (
    ReviewRequest,
    PredictionResponse
)

from backend.services.sentiment_service import SentimentService


router = APIRouter(
    prefix="/sentiment",
    tags=["Sentiment"]
)


@router.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(request: ReviewRequest):

    return SentimentService.predict(request.review)


@router.get("/reviews")
def get_reviews():

    return SentimentService.get_reviews()


@router.get("/stats")
def get_statistics():

    return SentimentService.get_statistics()


@router.get("/aspect-stats")
def get_aspect_statistics():

    return SentimentService.get_aspect_statistics()