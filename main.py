import pandas as pd
import os
import json
import time
import logging
from dotenv import load_dotenv
from openai import OpenAI
from pymongo import MongoClient, UpdateOne

# -----------------------------
# Logging
# -----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# -----------------------------
# Setup
# -----------------------------

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Missing OPENAI_API_KEY")

client_ai = OpenAI(api_key=api_key)

mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["ai_reviews_db"]
collection = db["reviews"]

# -----------------------------
# Load CSV
# -----------------------------

logging.info("Loading CSV...")
df = pd.read_csv("reviews.csv")

# -----------------------------
# Clean
# -----------------------------

df = df.dropna()
df["review"] = df["review"].str.strip()
df = df[df["review"] != ""]

# -----------------------------
# OpenAI Batch Sentiment
# -----------------------------

def get_sentiments_batch(reviews, retries=3):
    for attempt in range(retries):
        try:
            response = client_ai.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0,
                max_tokens=200,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a strict sentiment classifier. "
                            "Return ONLY a JSON array of strings. "
                            "Each value must be exactly one of: Positive, Negative, Neutral. "
                            "No explanations, no extra text."
                        )
                    },
                    {
                        "role": "user",
                        "content": json.dumps(reviews)
                    }
                ]
            )

            content = response.choices[0].message.content.strip()
            result = json.loads(content)

            if len(result) != len(reviews):
                raise ValueError("Mismatch between input and output length")

            return result

        except Exception as e:
            logging.warning(f"Attempt {attempt+1} failed: {e}")
            time.sleep(2 ** attempt)

    logging.error("Failed after retries - fallback used")
    return ["Neutral"] * len(reviews)

# -----------------------------
# Batch Processing
# -----------------------------

logging.info("Processing batches...")

batch_size = 20
sentiments = []

for i in range(0, len(df), batch_size):
    batch = df["review"].iloc[i:i+batch_size].tolist()
    result = get_sentiments_batch(batch)
    sentiments.extend(result)

df["sentiment"] = sentiments

# -----------------------------
# MongoDB Upsert
# -----------------------------

logging.info("Saving to MongoDB...")

operations = []

for record in df.to_dict("records"):
    operations.append(
        UpdateOne(
            {"review": record["review"]},
            {"$set": record},
            upsert=True
        )
    )

if operations:
    collection.bulk_write(operations)

# -----------------------------
# Verify data
# -----------------------------

logging.info("Sample data from MongoDB:")

for doc in collection.find().limit(5):
    logging.info(doc)

# -----------------------------
# Summary
# -----------------------------

print("\nSentiment Summary:\n")
print(df["sentiment"].value_counts())

logging.info("DONE")