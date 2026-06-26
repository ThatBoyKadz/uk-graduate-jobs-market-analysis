import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Page setup - this controls the browser tab title and layout
st.set_page_config(page_title="UK Graduate Data Jobs Market", layout="wide")

# Connect to our database
conn = sqlite3.connect("jobs.db")

# --- HEADER ---
st.title("UK Graduate Data & Tech Jobs Market")
st.markdown("An analysis of live UK graduate-level data analyst, data scientist, and tech job postings, built from real Reed.co.uk listings.")

# --- OVERVIEW STATS ROW ---
overview_query = """
SELECT 
    COUNT(*) as total_jobs,
    ROUND(AVG(minimumSalary), 0) as avg_min,
    ROUND(AVG(maximumSalary), 0) as avg_max
FROM jobs
WHERE minimumSalary IS NOT NULL
    AND minimumSalary >= 15000
    AND maximumSalary <= 70000
"""
overview = pd.read_sql(overview_query, conn).iloc[0]

total_jobs_query = "SELECT COUNT(*) as total FROM jobs"
total_jobs = pd.read_sql(total_jobs_query, conn).iloc[0]["total"]

col1, col2, col3 = st.columns(3)
col1.metric("Total Jobs Analysed", f"{total_jobs:,}")
col2.metric("Avg Min Salary", f"£{overview['avg_min']:,.0f}")
col3.metric("Avg Max Salary", f"£{overview['avg_max']:,.0f}")

st.divider()

# --- SKILLS BY SALARY CHART ---
st.subheader("Average Salary by Skill")

skills_query = """
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
"""
skills_df = pd.read_sql(skills_query, conn)

fig_skills = px.bar(
    skills_df,
    x="skill",
    y="avg_max_salary",
    text="job_count",
    labels={"skill": "Skill", "avg_max_salary": "Average Max Salary (£)"},
    title="Skills ranked by average maximum salary (label shows job count)"
)
fig_skills.update_traces(texttemplate="%{text} jobs", textposition="outside")
st.plotly_chart(fig_skills, use_container_width=True)

st.caption("Note: many jobs require multiple skills, so these categories overlap rather than being mutually exclusive.")

st.divider()

# --- TWO COLUMN LAYOUT: COMPANIES + LOCATIONS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Top Hiring Companies")
    companies_query = """
    SELECT employerName, COUNT(*) as job_count
    FROM jobs
    GROUP BY employerName
    ORDER BY job_count DESC
    LIMIT 10
    """
    companies_df = pd.read_sql(companies_query, conn)
    fig_companies = px.bar(
        companies_df,
        x="job_count",
        y="employerName",
        orientation="h",
        labels={"job_count": "Number of Postings", "employerName": ""}
    )
    fig_companies.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_companies, use_container_width=True)
    st.caption("Note: several top results are recruitment agencies posting on behalf of multiple clients, not direct employers.")

with col_right:
    st.subheader("Top Locations")
    locations_query = """
    SELECT locationName, COUNT(*) as job_count
    FROM jobs
    GROUP BY locationName
    ORDER BY job_count DESC
    LIMIT 10
    """
    locations_df = pd.read_sql(locations_query, conn)
    fig_locations = px.bar(
        locations_df,
        x="job_count",
        y="locationName",
        orientation="h",
        labels={"job_count": "Number of Postings", "locationName": ""}
    )
    fig_locations.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_locations, use_container_width=True)

conn.close()

st.divider()
st.caption("Data sourced from Reed.co.uk job postings API. Built by Danny Kadir.")