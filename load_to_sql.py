import pandas as pd
import sqlite3
import ast

# Load our cleaned data
df = pd.read_csv("clean_jobs.csv")

# The skills_found column is currently a string that LOOKS like a list,
# e.g. "['SQL', 'Excel']" - we need to convert it back into an actual Python list
df["skills_found"] = df["skills_found"].apply(ast.literal_eval)

# Connect to (or create) our SQLite database file
conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

# Create the jobs table - one row per job
cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    jobId INTEGER PRIMARY KEY,
    jobTitle TEXT,
    employerName TEXT,
    locationName TEXT,
    minimumSalary REAL,
    maximumSalary REAL,
    currency TEXT,
    date TEXT,
    jobUrl TEXT
)
""")

# Create the job_skills table - one row per job-skill pairing
cursor.execute("""
CREATE TABLE IF NOT EXISTS job_skills (
    jobId INTEGER,
    skill TEXT,
    FOREIGN KEY (jobId) REFERENCES jobs (jobId)
)
""")

# Clear out any existing data, in case we run this script more than once
cursor.execute("DELETE FROM jobs")
cursor.execute("DELETE FROM job_skills")

# Insert each job into the jobs table
jobs_data = df[[
    "jobId", "jobTitle", "employerName", "locationName",
    "minimumSalary", "maximumSalary", "currency", "date", "jobUrl"
]].values.tolist()

cursor.executemany("""
INSERT INTO jobs (jobId, jobTitle, employerName, locationName, minimumSalary, maximumSalary, currency, date, jobUrl)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", jobs_data)

# Insert each job-skill pairing into job_skills
skill_rows = []
for _, row in df.iterrows():
    for skill in row["skills_found"]:
        skill_rows.append((row["jobId"], skill))

cursor.executemany("INSERT INTO job_skills (jobId, skill) VALUES (?, ?)", skill_rows)

conn.commit()

print(f"Loaded {len(jobs_data)} jobs into the jobs table")
print(f"Loaded {len(skill_rows)} job-skill pairings into the job_skills table")

# Quick test query - top 5 most mentioned skills
cursor.execute("""
SELECT skill, COUNT(*) as count
FROM job_skills
GROUP BY skill
ORDER BY count DESC
LIMIT 5
""")
print("\nTop 5 skills by mentions:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

conn.close()