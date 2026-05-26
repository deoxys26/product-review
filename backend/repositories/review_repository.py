from collections import Counter

from backend.database.database import SessionLocal
from backend.database.models import Review


class ReviewRepository:

    @staticmethod
    def save_review(review_text, sentiment, confidence):

        db = SessionLocal()

        review = Review(
            review_text=review_text,
            sentiment=sentiment,
            confidence=confidence
        )

        db.add(review)
        db.commit()
        db.close()

    @staticmethod
    def get_all_reviews():

        db = SessionLocal()

        reviews = db.query(Review).all()

        result = []

        for review in reviews:
            result.append({
                "id": review.id,
                "review_text": review.review_text,
                "sentiment": review.sentiment,
                "confidence": review.confidence
            })

        db.close()

        return result

    @staticmethod
    def get_statistics():

        db = SessionLocal()

        positive = db.query(Review).filter(
            Review.sentiment == "Positive"
        ).count()

        negative = db.query(Review).filter(
            Review.sentiment == "Negative"
        ).count()

        total = positive + negative

        db.close()

        return {
            "total": total,
            "positive": positive,
            "negative": negative
        }

    @staticmethod
    def get_aspect_statistics():

        db = SessionLocal()

        reviews = db.query(Review).all()

        aspect_keywords = [
            "battery",
            "camera",
            "display",
            "screen",
            "charging",
            "heating",
            "performance",
            "delivery",
            "price",
            "speaker"
        ]

        counter = Counter()

        for review in reviews:
            text = review.review_text.lower()

            for aspect in aspect_keywords:
                if aspect in text:
                    counter[aspect] += 1

        db.close()

        return dict(counter)