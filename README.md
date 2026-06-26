# UK Graduate Data & Tech Jobs Market Analysis

An end-to-end data project analysing live UK graduate-level data analyst, data scientist, and tech job postings — built while actively job hunting, to understand what skills are actually in demand and what they pay.

🔗 **[Live Dashboard](your-streamlit-link-goes-here)**

## What it does

- Pulls live job postings from the Reed.co.uk Jobs API across multiple graduate-relevant search terms (data analyst, data scientist, data engineer, graduate schemes, etc.)
- Cleans and deduplicates the data, then extracts mentioned skills (Python, SQL, Excel, Power BI, AWS, etc.) from full job descriptions using text matching
- Loads the cleaned data into a normalized SQLite database (separate `jobs` and `job_skills` tables)
- Runs analytical SQL queries to surface insights: average salary by skill, top hiring companies, top locations, overall market salary stats
- Presents everything in an interactive Streamlit dashboard

## Key findings

- **388 jobs** had usable salary data in a realistic graduate range (£16k–£70k), averaging **£31k–£39k**
- **Python** was the most mentioned skill (173 of 532 jobs), but **Tableau** and **SQL** roles had the highest average salaries
- **London** dominates by volume (69 jobs), followed by Manchester and Leeds
- Many top "hiring companies" are recruitment agencies posting on behalf of multiple clients, not direct employers — an important caveat for interpreting the data

## Tech stack

- **Python** (requests, pandas) — data collection and cleaning
- **SQL** (SQLite) — normalized relational database design
- **Streamlit + Plotly** — interactive dashboard
- **Reed.co.uk Jobs API** — live data source

## Project structure



## Limitations

- Skill categories overlap (a job can require multiple skills), so skill-salary comparisons aren't strictly independent
- Salary data was only available for ~73% of postings; figures reflect that subset
- Snapshot-based: reflects job postings live at the time of collection, not a continuous feed

## Author

Danny Kadir — [LinkedIn](https://www.linkedin.com/in/danny-kadir-940274413/) 
