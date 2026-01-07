import requests
import json
import random
import os
from dotenv import load_dotenv

# 1) load the .env file now
load_dotenv()

# 2) then grab your key
serper_key = os.getenv('SERPER_API')
if not serper_key:
    raise RuntimeError("SERPER_API not set in environment or .env file")

# Load your API keys
SERPER_API_KEYS = [
    serper_key,
]

SEARCH_URL = "https://google.serper.dev/search"

def google_search_serper(query):
    key = random.choice(SERPER_API_KEYS)  # rotate randomly
    headers = {
        "X-API-KEY": key,
        "Content-Type": "application/json"
    }
    data = {
        "q": query
    }

    try:
        response = requests.post(SEARCH_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        results = response.json()
        urls = []
        if "organic" in results:
            for item in results["organic"]:
                url = item.get("link")
                if url:
                    urls.append(url)
        return urls
    except Exception as e:
        print(f"Error querying Serper API: {e}")
        return []
