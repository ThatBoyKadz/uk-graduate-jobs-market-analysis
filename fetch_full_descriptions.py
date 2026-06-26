import json
import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()
API_KEY = os.getenv("REED_API_KEY")

# Load the raw jobs we already collected
with open("raw_jobs.json", "r", encoding="utf-8") as f:
    raw_jobs = json.load(f)

# Remove duplicates by jobId first - no point fetching the same job twice
seen_ids = set()
unique_jobs = []
for job in raw_jobs:
    if job["jobId"] not in seen_ids:
        seen_ids.add(job["jobId"])
        unique_jobs.append(job)

print(f"Fetching full descriptions for {len(unique_jobs)} unique jobs...")
print("This will take a while - roughly 1 second per job. Feel free to let it run.")

full_jobs = []
errors = 0

for i, job in enumerate(unique_jobs):
    job_id = job["jobId"]
    url = f"https://www.reed.co.uk/api/1.0/jobs/{job_id}"
    
    response = requests.get(url, auth=(API_KEY, ""))
    
    if response.status_code == 200:
        full_data = response.json()
        # Replace the short description with the full one
        job["jobDescription"] = full_data.get("jobDescription", job["jobDescription"])
        full_jobs.append(job)
    else:
        errors += 1
        full_jobs.append(job)  # keep the short version if the fetch failed
    
    # Print progress every 50 jobs so we know it's alive
    if (i + 1) % 50 == 0:
        print(f"  Progress: {i + 1}/{len(unique_jobs)} done")
    
    time.sleep(1)

print(f"\nDone. {errors} jobs had errors fetching full description (kept short version for those).")

# Save the updated data with full descriptions
with open("raw_jobs_full.json", "w", encoding="utf-8") as f:
    json.dump(full_jobs, f, indent=2)

print("Saved to raw_jobs_full.json")