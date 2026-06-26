import sqlite3

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

print("=" * 50)
print("QUERY 1: Average salary by skill")
print("=" * 50)

cursor.execute("""
SELECT 
    js.skill,
    COUNT(*) as job_count,
    ROUND(AVG(j.minimumSalary), 0) as avg_min_salary,
    ROUND(AVG(j.maximumSalary), 0) as avg_max_salary
FROM job_skills js
JOIN jobs j ON js.jobId = j.jobId
WHERE j.minimumSalary IS NOT NULL
    AND j.minimumSalary >= 15000
    AND j.maximumSalary <= 70000
GROUP BY js.skill
HAVING job_count >= 10
ORDER BY avg_max_salary DESC
""")

for row in cursor.fetchall():
    print(f"{row[0]:20} | jobs: {row[1]:4} | avg min: £{row[2]:>8,.0f} | avg max: £{row[3]:>8,.0f}")

print("\n" + "=" * 50)
print("QUERY 2: Top 10 hiring companies")
print("=" * 50)

cursor.execute("""
SELECT employerName, COUNT(*) as job_count
FROM jobs
GROUP BY employerName
ORDER BY job_count DESC
LIMIT 10
""")

for row in cursor.fetchall():
    print(f"{row[0]:40} | {row[1]} jobs")

print("\n" + "=" * 50)
print("QUERY 3: Top locations by job count")
print("=" * 50)

cursor.execute("""
SELECT locationName, COUNT(*) as job_count
FROM jobs
GROUP BY locationName
ORDER BY job_count DESC
LIMIT 10
""")

for row in cursor.fetchall():
    print(f"{row[0]:30} | {row[1]} jobs")

print("\n" + "=" * 50)
print("QUERY 4: Overall salary stats (realistic graduate range only)")
print("=" * 50)

cursor.execute("""
SELECT 
    COUNT(*) as total_with_salary,
    ROUND(AVG(minimumSalary), 0) as avg_min,
    ROUND(AVG(maximumSalary), 0) as avg_max,
    ROUND(MIN(minimumSalary), 0) as lowest,
    ROUND(MAX(maximumSalary), 0) as highest
FROM jobs
WHERE minimumSalary IS NOT NULL
    AND minimumSalary >= 15000
    AND maximumSalary <= 70000
""")

row = cursor.fetchone()
print(f"Jobs with salary in realistic graduate range: {row[0]}")
print(f"Average min salary: £{row[1]:,.0f}")
print(f"Average max salary: £{row[2]:,.0f}")
print(f"Lowest salary seen: £{row[3]:,.0f}")
print(f"Highest salary seen: £{row[4]:,.0f}")

conn.close()