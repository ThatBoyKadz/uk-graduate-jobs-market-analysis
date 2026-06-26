import requests
import os
from dotenv import load_dotenv
import json
import time

load_dotenv()
API_KEY = os.getenv("REED_API_KEY")

url = "https://www.reed.co.uk/api/1.0/search"

keywords_list = [
    "graduate data analyst",
    "graduate data scientist",
    "data analyst",
    "data scientist",
    "graduate scheme data",
    "business analyst graduate",
    "data engineer graduate"
]

all_jobs = []

for keyword in keywords_list:
    print(f"Searching: '{keyword}'...")
    params = {
        "keywords": keyword,
        "resultsToTake": 100
    }
    response = requests.get(url, params=params, auth=(API_KEY, ""))
    if response.status_code == 200:
        data = response.json()
        jobs_found = data["results"]
        print(f"  -> Found {data['totalResults']} total, pulled {len(jobs_found)}")
        all_jobs.extend(jobs_found)
    else:
        print(f"  -> Error: {response.status_code}")
    time.sleep(1)

print(f"\nTotal jobs collected (before removing duplicates): {len(all_jobs)}")

with open("raw_jobs.json", "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, indent=2)

print("Saved to raw_jobs.json")