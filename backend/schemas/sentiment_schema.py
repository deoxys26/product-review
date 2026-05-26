from pydantic import BaseModel
from typing import List


class ReviewRequest(BaseModel):
    review: str


class PredictionResponse(BaseModel):
    review: str
    normalized_review: str
    sentiment: str
    confidence: float
    aspects: List[str]