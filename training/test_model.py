from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="./saved_model",
    tokenizer="./saved_model"
)

reviews = [
    "This laptop is amazing",
    "Worst product I have ever bought",
    "Battery life is fantastic",
    "Waste of money"
]

for review in reviews:
    result = classifier(review)[0]

    print("\nReview:", review)
    print("Prediction:", result)