
import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="IPL Data Analysis Dashboard",
    page_icon="🏏",
    layout="wide"
)

# Title
st.title("🏏 IPL Cricket Data Analysis Dashboard")
st.caption("Explore IPL statistics, player performance and team records")

st.divider()

# Load Datasets
matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")

# Convert numeric columns safely
deliveries["runs_off_bat"] = pd.to_numeric(
    deliveries["runs_off_bat"], errors="coerce"
).fillna(0)

deliveries["extras"] = pd.to_numeric(
    deliveries["extras"], errors="coerce"
).fillna(0)

# Dashboard Statistics
total_matches = matches["match_id"].nunique()

total_runs = (
    deliveries["runs_off_bat"].sum()
    + deliveries["extras"].sum()
)

total_teams = deliveries["batting_team"].nunique()
total_players = deliveries["striker"].nunique()

# Metric Cards
st.subheader("📊 IPL Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Matches", f"{total_matches:,}")
col2.metric("Total Runs", f"{total_runs:,}")
col3.metric("Total Teams", total_teams)
col4.metric("Total Batters", total_players)

st.divider()

# Top Run Scorers
st.subheader("🏆 Top 10 Run Scorers")

top_scorers = (
    deliveries.groupby("striker")["runs_off_bat"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_scorers)

st.divider()

# Top Wicket Takers
st.subheader("🎯 Top 10 Wicket Takers")

wicket_data = deliveries[
    deliveries["wicket_type"].notna()
    & ~deliveries["wicket_type"].isin([
        "run out",
        "retired hurt",
        "obstructing the field",
        "retired out"
    ])
]

top_wickets = (
    wicket_data.groupby("bowler")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_wickets)

st.divider()

# Season-wise Total Runs
st.subheader("📈 Season-wise Total Runs")

deliveries["season"] = deliveries["season"].astype(str)

deliveries["total_runs"] = (
    deliveries["runs_off_bat"] + deliveries["extras"]
)

season_runs = (
    deliveries.groupby("season")["total_runs"]
    .sum()
    .sort_index()
)

st.line_chart(season_runs)

st.divider()

# Team-wise Match Wins
st.subheader("🏅 Team-wise Match Wins")

team_wins = (
    matches.groupby("winner")["match_id"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(team_wins)

st.divider()

# Toss Decision Analysis
st.subheader("🪙 Toss Decision Analysis")

toss_data = matches["toss_decision"].value_counts()

col1, col2 = st.columns(2)

with col1:
    st.write("Toss Decision Statistics")
    st.dataframe(toss_data, use_container_width=True)

with col2:
    st.write("Toss Decision Chart")
    st.bar_chart(toss_data)

st.divider()

# Player of the Match
st.subheader("⭐ Top 10 Player of the Match")

player_awards = (
    matches["player_of_match"]
    .dropna()
    .value_counts()
    .head(10)
)

st.bar_chart(player_awards)

st.divider()

# Footer
st.caption("IPL Cricket Data Analysis Project | Built using Python, Pandas and Streamlit")
