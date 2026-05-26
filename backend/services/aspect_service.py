class AspectService:

    ASPECTS = [
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

    @staticmethod
    def extract(review: str):

        review = review.lower()

        detected = []

        for aspect in AspectService.ASPECTS:

            if aspect in review:
                detected.append(aspect)

        return detected