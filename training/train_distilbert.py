import pandas as pd
import torch

from sklearn.model_selection import train_test_split

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)

# ======================================
# LOAD DATA
# ======================================

df = pd.read_csv("data/cleaned_reviews.csv")

print(df.head())
print(df.shape)

# Remove null values

df = df.dropna(
    subset=["clean_review", "label"]
)

# Ensure label is integer

df["label"] = df["label"].astype(int)

print(df["label"].value_counts())

# ======================================
# TRAIN TEST SPLIT
# ======================================

train_df, test_df = train_test_split(
    df,
    test_size=0.2,
    random_state=42,
    stratify=df["label"]
)

# ======================================
# TOKENIZER
# ======================================

tokenizer = AutoTokenizer.from_pretrained(
    "distilbert-base-uncased"
)

train_encodings = tokenizer(
    train_df["clean_review"].tolist(),
    truncation=True,
    padding=True,
    max_length=128
)

test_encodings = tokenizer(
    test_df["clean_review"].tolist(),
    truncation=True,
    padding=True,
    max_length=128
)

# ======================================
# DATASET CLASS
# ======================================

class ReviewDataset(torch.utils.data.Dataset):

    def __init__(self, encodings, labels):

        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):

        item = {
            key: torch.tensor(val[idx])
            for key, val in self.encodings.items()
        }

        item["labels"] = torch.tensor(
            self.labels[idx]
        )

        return item

    def __len__(self):

        return len(self.labels)

# ======================================
# DATASETS
# ======================================

train_dataset = ReviewDataset(
    train_encodings,
    train_df["label"].tolist()
)

test_dataset = ReviewDataset(
    test_encodings,
    test_df["label"].tolist()
)

# ======================================
# MODEL
# ======================================

model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2
)

# ======================================
# TRAINING ARGUMENTS
# ======================================

training_args = TrainingArguments(
    output_dir="./results",

    num_train_epochs=2,

    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,

    eval_strategy="epoch",

    save_strategy="epoch",

    logging_dir="./logs",

    logging_steps=50
)

# ======================================
# TRAINER
# ======================================

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)

# ======================================
# TRAIN
# ======================================

trainer.train()

# ======================================
# SAVE MODEL
# ======================================

model.save_pretrained("saved_model")
tokenizer.save_pretrained("saved_model")

print("Model Saved Successfully")