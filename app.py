
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Advanced IPL Dashboard",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 Advanced IPL Cricket Data Analysis")
st.caption("Explore IPL matches, teams, players and performance")

# Load datasets
@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv")

    matches["season"] = matches["season"].astype(str)
    deliveries["season"] = deliveries["season"].astype(str)

    for col in ["runs_off_bat", "extras"]:
        deliveries[col] = pd.to_numeric(
            deliveries[col], errors="coerce"
        ).fillna(0)

    return matches, deliveries

matches, deliveries = load_data()

# Sidebar filters
st.sidebar.header("Dashboard Filters")

seasons = sorted(deliveries["season"].dropna().unique())
selected_seasons = st.sidebar.multiselect(
    "Select Season",
    seasons,
    default=seasons
)

teams = sorted(deliveries["batting_team"].dropna().unique())
selected_teams = st.sidebar.multiselect(
    "Select Teams",
    teams,
    default=teams
)

players = sorted(deliveries["striker"].dropna().unique())
selected_players = st.sidebar.multiselect(
    "Select Players",
    players
)

filtered = deliveries[
    deliveries["season"].isin(selected_seasons)
    & deliveries["batting_team"].isin(selected_teams)
].copy()

# Overview
st.header("1. IPL Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Matches", len(matches))
col2.metric("Total Runs", int(
    deliveries["runs_off_bat"].sum() + deliveries["extras"].sum()
))
col3.metric("Total Teams", deliveries["batting_team"].nunique())
col4.metric("Total Players", deliveries["striker"].nunique())

st.divider()

# Top Run Scorers
st.header("2. Top 10 Run Scorers")

runs = (
    filtered.groupby("striker")["runs_off_bat"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(runs)

# Top Wicket Takers
st.header("3. Top 10 Wicket Takers")

valid_wickets = filtered[
    filtered["wicket_type"].notna()
    & ~filtered["wicket_type"].isin(
        ["run out", "retired hurt", "obstructing the field"]
    )
]

wickets = (
    valid_wickets.groupby("bowler")["wicket_type"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(wickets)

# Season-wise Runs
st.header("4. Season-wise Total Runs")

season_runs = (
    filtered.groupby("season")
    .apply(
        lambda x: x["runs_off_bat"].sum() + x["extras"].sum(),
        include_groups=False
    )
)

st.line_chart(season_runs)

# Team Wins
st.header("5. Team-wise Match Wins")

if "winner" in matches.columns:
    team_wins = (
        matches[matches["winner"].isin(selected_teams)]
        ["winner"].value_counts()
    )
    st.bar_chart(team_wins)

# Orange Cap
st.header("6. Orange Cap Analysis")

orange_cap = (
    filtered.groupby(["season", "striker"])["runs_off_bat"]
    .sum()
    .reset_index()
    .sort_values("runs_off_bat", ascending=False)
    .groupby("season")
    .head(1)
)

st.dataframe(orange_cap,width="stretch" )

# Purple Cap
st.header("7. Purple Cap Analysis")

purple_cap = (
    valid_wickets.groupby(["season", "bowler"])
    .size()
    .reset_index(name="wickets")
    .sort_values("wickets", ascending=False)
    .groupby("season")
    .head(1)
)

st.dataframe(purple_cap, use_container_width=True)

# Batting Strike Rate
st.header("8. Batting Performance")

batting = (
    filtered.groupby("striker")
    .agg(
        runs=("runs_off_bat", "sum"),
        balls=("actual_delivery", "count")
    )
)

batting["strike_rate"] = np.where(
    batting["balls"] > 0,
    batting["runs"] / batting["balls"] * 100,
    0
)

st.dataframe(
    batting.sort_values("runs", ascending=False).head(10),
    use_container_width=True
)

# Bowling Economy
st.header("9. Bowling Performance")

bowling = (
    filtered.groupby("bowler")
    .agg(
        runs_conceded=("runs_off_bat", "sum"),
        balls=("actual_delivery", "count")
    )
)

bowling["economy"] = np.where(
    bowling["balls"] > 0,
    bowling["runs_conceded"] * 6 / bowling["balls"],
    0
)

st.dataframe(
    bowling.sort_values("economy").head(10),
    use_container_width=True
)

# Venue Analysis
st.header("10. Venue Analysis")

venue_matches = matches["venue"].value_counts().head(10)
st.bar_chart(venue_matches)

# Toss Impact
st.header("11. Toss Impact Analysis")

if "toss_winner" in matches.columns and "winner" in matches.columns:
    toss_wins = matches[
        matches["toss_winner"] == matches["winner"]
    ]
    st.metric("Matches Won by Toss Winners", len(toss_wins))

# Player Selection
st.header("12. Player Analysis")

if selected_players:
    player_data = filtered[
        filtered["striker"].isin(selected_players)
    ]

    player_runs = (
        player_data.groupby("striker")["runs_off_bat"]
        .sum()
    )

    st.bar_chart(player_runs)
else:
    st.info("Select players from the sidebar to compare their runs.")

st.divider()
st.caption("IPL Cricket Data Analysis | Python • Pandas • Streamlit")
