from config import API_KEY, COUNTRIES, BASE_URL, MAX_RESULTS 
import requests
from pymongo import MongoClient
import os
from datetime import datetime

# MongoDB connection 
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://subhakantarath:Subhakanta%40123@cluster0.39afqqe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client["youtube_trends"]

def fetch_trending_videos(region_code):
    """Fetch trending videos from YouTube API for specific region"""
    try:
        url = f"{BASE_URL}?part=snippet,statistics,contentDetails&chart=mostPopular&regionCode={region_code}&maxResults={MAX_RESULTS}&key={API_KEY}"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json().get("items", [])
    except Exception as e:
        print(f"API Error for {region_code}: {e}")
        return []

def save_to_mongodb(data, country_name):
    """Save video data directly to MongoDB with metadata"""
    if data:
        collection_name = f"{country_name.lower()}_trending"
        collection = db[collection_name]
        
        # Add metadata to each video
        for item in data:
            item['fetch_date'] = datetime.now()
            item['country'] = country_name
        
        collection.insert_many(data)
        print(f" Inserted {len(data)} videos for {country_name}")
    else:
        print(f" No data for {country_name}")

def fetch_and_store_all():
    """Main function to fetch and store data for all countries"""
    for cname, ccode in COUNTRIES.items():
        print(f" Processing {cname}...")
        videos = fetch_trending_videos(ccode)
        save_to_mongodb(videos, cname)


if __name__ == "__main__":
    fetch_and_store_all()