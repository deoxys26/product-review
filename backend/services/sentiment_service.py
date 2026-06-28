import os
import requests

from backend.repositories.review_repository import ReviewRepository
from backend.services.aspect_service import AspectService

# Explicitly routing through the new Hugging Face core router
HF_API_URL = "https://router.huggingface.co/hf-inference/models/deoxys26/amazon-sentiment-distilbert"
HF_TOKEN = os.getenv("HF_TOKEN")

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
    normalized_words = [slang_map.get(word, word) for word in words]
    return " ".join(normalized_words)

def query_huggingface(text: str):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # The new router endpoint expects the raw single input wrapper
    payload = {"inputs": text}

    try:
        response = requests.post(
            HF_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except StopIteration as e:
        # Prevents Python 3.14 from turning internal iterator closures into coroutine RuntimeErrors
        raise RuntimeError(f"Internal loop processing error: {e}")

class SentimentService:

    @staticmethod
    def predict(review: str):
        normalized_review = normalize_text(review)
        result = query_huggingface(normalized_review)

        # Safeguard array parsing structures safely
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], list):
                prediction = max(result[0], key=lambda x: x["score"])
            else:
                prediction = result[0]
        else:
            raise ValueError(f"Unexpected response format from AI model router: {result}")

        sentiment = (
            "Positive"
            if prediction["label"] == "LABEL_1"
            else "Negative"
        )

        confidence = round(prediction["score"], 4)
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