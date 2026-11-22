import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="IPL Data Analysis Dashboard",
    layout="wide"
)

st.title("IPL Cricket Data Analysis Dashboard")

st.write("Welcome to IPL Data Analysis Project!")

# Load datasets
matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")

st.success("IPL Datasets Loaded Successfully!")

# Dashboard statistics
total_matches = matches["match_id"].nunique()

total_runs = (
    deliveries["runs_off_bat"].sum()
    + deliveries["extras"].sum()
)

total_teams = deliveries["batting_team"].nunique()

total_players = deliveries["striker"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Matches", total_matches)
col2.metric("Total Runs", total_runs)
col3.metric("Total Teams", total_teams)
col4.metric("Total Batters", total_players)
st.subheader("Top 10 Run Scorers")

top_scorers = (
    deliveries.groupby("striker")["runs_off_bat"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_scorers)
st.subheader("Top 10 Wicket Takers")

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
st.subheader("Season-wise Total Runs")
deliveries["season"] = deliveries["season"].astype(str)

deliveries["total_runs"] = (
    pd.to_numeric(deliveries["runs_off_bat"], errors="coerce").fillna(0)
    + pd.to_numeric(deliveries["extras"], errors="coerce").fillna(0)
)
st.subheader("Season-wise Total Runs")

deliveries["season"] = deliveries["season"].astype(str)

deliveries["total_runs"] = (
    pd.to_numeric(deliveries["runs_off_bat"], errors="coerce").fillna(0)
    + pd.to_numeric(deliveries["extras"], errors="coerce").fillna(0)
)

season_runs = (
    deliveries.groupby("season")["total_runs"]
    .sum()
    .sort_index()
)

st.line_chart(season_runs)


st.subheader("Team-wise Match Wins")

team_wins = matches.groupby("winner")["match_id"].count()

team_wins = team_wins.sort_values(ascending=False).head(10)

st.bar_chart(team_wins)


st.subheader("Toss Decision Analysis")

toss_data = matches["toss_decision"].value_counts()

st.write("Toss Decision Statistics")

st.dataframe(toss_data)

st.vega_lite_chart(
    toss_data.reset_index(),
    {
        "mark": {"type": "arc", "innerRadius": 0},
        "encoding": {
            "theta": {"field": "count", "type": "quantitative"},
            "color": {"field": "toss_decision", "type": "nominal"}
        }
    }
)
st.subheader("Top 10 Player of the Match")

player_awards = (
    matches["player_of_match"]
    .dropna()
    .value_counts()
    .head(10)
)

st.bar_chart(player_awards)
