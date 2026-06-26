import json
import pandas as pd
import re

# Load the raw data we collected
with open("raw_jobs_full.json", "r", encoding="utf-8") as f:
    raw_jobs = json.load(f)

print(f"Loaded {len(raw_jobs)} raw job entries")

# Convert to a pandas DataFrame - this is like turning it into a spreadsheet table
df = pd.DataFrame(raw_jobs)

# Remove duplicates - same job can appear from multiple keyword searches
df = df.drop_duplicates(subset="jobId")
print(f"After removing duplicates: {len(df)} unique jobs")

# Keep only the columns we actually need
df = df[[
    "jobId", "jobTitle", "employerName", "locationName",
    "minimumSalary", "maximumSalary", "currency",
    "date", "jobDescription", "jobUrl"
]]

# The skills we're going to search for in title + description
skills_list = [
    "Python", "SQL", "Excel", "Power BI", "Tableau", "R",
    "AWS", "Azure", "Java", "JavaScript", "Machine Learning",
    "Statistics", "A/B Testing", "ETL", "Snowflake", "Spark"
]

def find_skills(text):
    """Search a piece of text and return which skills from our list appear in it."""
    if not isinstance(text, str):
        return []
    found = []
    for skill in skills_list:
        # case-insensitive search, word boundaries to avoid partial matches like 'R' inside 'Director'
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            found.append(skill)
    return found

# Combine title + description into one field to search across both
df["combined_text"] = df["jobTitle"].fillna("") + " " + df["jobDescription"].fillna("")
df["skills_found"] = df["combined_text"].apply(find_skills)

# Drop the helper column, we don't need it in the final output
df = df.drop(columns=["combined_text"])

# Save the cleaned data
df.to_csv("clean_jobs.csv", index=False)
print("Saved cleaned data to clean_jobs.csv")

# Quick preview of what we found
print("\nSample skills found across jobs:")
print(df["skills_found"].head(10))
