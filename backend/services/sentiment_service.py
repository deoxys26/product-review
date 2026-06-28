import os
import requests

from backend.repositories.review_repository import ReviewRepository
from backend.services.aspect_service import AspectService


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

    normalized_words = [
        slang_map.get(word, word)
        for word in words
    ]

    return " ".join(normalized_words)


import os
from huggingface_hub import InferenceClient

from backend.repositories.review_repository import ReviewRepository
from backend.services.aspect_service import AspectService

# Initialize the official Hugging Face client
# (It manages the entire connection architecture securely using your token)
HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(token=HF_TOKEN)

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

# We replace the old manual request block with this clean SDK call
def query_huggingface(text: str):
    # This automatically structures the exact JSON payload the router demands
    return client.text_classification(
        text, 
        model="deoxys26/amazon-sentiment-distilbert"
    )

# ... (The rest of your SentimentService class remains exactly the same!)


class SentimentService:

    @staticmethod
    def predict(review: str):

        normalized_review = normalize_text(review)

        result = query_huggingface(normalized_review)

        # Hugging Face may return [[{label, score}, ...]]
        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
            prediction = max(result[0], key=lambda x: x["score"])
        else:
            prediction = result[0]

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