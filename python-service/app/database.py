from pymongo import MongoClient
import os

# MongoDB connection setup
client = MongoClient("mongodb+srv://khushichoudhary1107:Khushi123@cluster0.n31bj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Database and collection selection
expert_db = client["expert_database"]
expert_collection = expert_db["experts"]

candidate_db = client["candidate_database"]
candidates_collection = candidate_db["candidates"]

def get_candidates():
    """Fetch all candidates from the MongoDB collection."""
    return list(candidates_collection.find({}))

def get_experts():
    """Fetch all experts from the MongoDB collection."""
    return list(expert_collection.find({}))
