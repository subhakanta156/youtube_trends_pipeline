from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")  # fallback for local
client = MongoClient(MONGO_URI)

db = client["youtube_trends"]  # Use your DB name here
