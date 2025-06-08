# dashboard.py

import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

st.title("📊 Online Course Engagement Dashboard")

# Total Minutes Watched
st.header("⏱️ Total Minutes Watched")
total_res = requests.get(f"{BASE_URL}/total_minutes").json()
st.metric(label="Total Minutes", value=int(total_res["total_minutes_watched"]))

# Top 3 Courses
st.header("🏆 Top 3 Courses by Engagement")
top_res = requests.get(f"{BASE_URL}/top_courses").json()
top_df = pd.DataFrame(top_res)
st.bar_chart(top_df.set_index("course"))

# Daily Engagement
st.header("📅 Daily Engagement")
daily_res = requests.get(f"{BASE_URL}/daily_engagement").json()
daily_df = pd.DataFrame(daily_res)
daily_df["date"] = pd.to_datetime(daily_df["date"])
daily_df = daily_df.sort_values("date")
st.line_chart(daily_df.set_index("date"))

# Average Quiz Score per Course
st.header("🧠 Average Quiz Scores")
score_res = requests.get(f"{BASE_URL}/average_scores").json()
score_df = pd.DataFrame(score_res)
st.bar_chart(score_df.set_index("course"))

st.caption("Built with FastAPI + Streamlit + PostgreSQL 💡")
