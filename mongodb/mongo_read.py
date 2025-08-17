import sys
import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

# Set path to access config & env
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_ingestion.config import COUNTRIES

load_dotenv()

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["youtube_trends"]

def export_mongo_to_csv():
    for country in COUNTRIES.keys():
        collection_name = f"{country.lower()}_trending"
        collection = db[collection_name]

        data = list(collection.find())
        if not data:
            print(f" No data found for {country}")
            continue

        # Remove MongoDB internal _id if present
        for doc in data:
            doc.pop("_id", None)

        df = pd.DataFrame(data)

        # Create folder path
        folder_path = os.path.join("data", "processed")
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, f"{country.lower()}_trending.csv")
        df.to_csv(file_path, index=False, encoding="utf-8")
        print(f" Saved CSV for {country} → {file_path}")

if __name__ == "__main__":
    export_mongo_to_csv()
