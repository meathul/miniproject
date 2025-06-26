import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME", "smartreco")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "user_profiles")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def store_user_profile(user_id: str, profile_data: dict):
    """Store or update a user profile in MongoDB."""
    collection.update_one(
        {"user_id": user_id},
        {"$set": {"profile": profile_data}},
        upsert=True
    )

def get_user_profile(user_id: str) -> dict:
    """Retrieve a user profile from MongoDB."""
    doc = collection.find_one({"user_id": user_id})
    return doc["profile"] if doc and "profile" in doc else None 