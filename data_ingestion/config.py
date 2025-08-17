import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY environment variable not set!")
COUNTRIES = {
    "India": "IN", 
    "USA": "US",
    "Singapore": "SG"
}
BASE_URL = "https://www.googleapis.com/youtube/v3/videos"
MAX_RESULTS = 50