from pathlib import Path
from transformers import pipeline

from backend.repositories.review_repository import ReviewRepository
from backend.services.aspect_service import AspectService

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "saved_model"

classifier = pipeline(
    "sentiment-analysis",
    model=str(MODEL_PATH),
    tokenizer=str(MODEL_PATH)
)


def normalize_text(text: str):
    slang_map = {
        "goated": "excellent",
        "goat": "excellent",
        "fire": "excellent",
        "lit": "excellent",
        "dope": "excellent",
        "trash": "terrible",
        "mid": "average",
        "sucks": "terrible",
        "worst": "terrible",
        "bad": "terrible"
    }

    words = text.lower().split()

    normalized_words = [
        slang_map.get(word, word)
        for word in words
    ]

    return " ".join(normalized_words)


class SentimentService:

    @staticmethod
    def predict(review: str):

        normalized_review = normalize_text(review)

        result = classifier(normalized_review)[0]

        sentiment = (
            "Positive"
            if result["label"] == "LABEL_1"
            else "Negative"
        )

        confidence = round(result["score"], 4)

        aspects = AspectService.extract(review)

        ReviewRepository.save_review(
            review_text=review,
            sentiment=sentiment,
            confidence=confidence
        )

        return {
            "review": review,
            "normalized_review": normalized_review,
            "sentiment": sentiment,
            "confidence": confidence,
            "aspects": aspects
        }

    @staticmethod
    def get_reviews():

        return ReviewRepository.get_all_reviews()

    @staticmethod
    def get_statistics():

        return ReviewRepository.get_statistics()

    @staticmethod
    def get_aspect_statistics():

        return ReviewRepository.get_aspect_statistics()