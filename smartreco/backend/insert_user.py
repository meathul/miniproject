import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB_NAME", "smartreco")]
collection = db[os.getenv("MONGO_COLLECTION_NAME", "user_profiles")]

user_profile = {
    "user_id": "59b99ddacfa9a34dcd7885fc",
    "profile": {
        "skin_type": "dry",
        "age": 25,
        "ethnicity": "asian",
        "budget": 1000,
        "preferred_brands": []
    }
}

collection.update_one(
    {"user_id": user_profile["user_id"]},
    {"$set": user_profile},
    upsert=True
)

print("User profile inserted/updated!") 