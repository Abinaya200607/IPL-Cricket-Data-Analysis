import pandas as pd
import os
import glob

folder_path = os.path.expanduser(
    "~/Downloads/ipl_male_csv2"
)

delivery_files = glob.glob(
    os.path.join(folder_path, "*.csv")
)

delivery_files = [
    f for f in delivery_files
    if not f.endswith("_info.csv")
]

all_deliveries = []

for file in delivery_files:
    df = pd.read_csv(file)
    all_deliveries.append(df)

deliveries = pd.concat(
    all_deliveries,
    ignore_index=True
)

deliveries.to_csv("deliveries.csv", index=False)

print("Deliveries CSV Created!")
print(deliveries.shape)
# Create Matches CSV

import csv

info_files = glob.glob(
    os.path.join(folder_path, "*_info.csv")
)

all_matches = []

for file in info_files:

    match = {
    "match_id": os.path.basename(file).replace("_info.csv", "").split(" | ")[0]    
    }

    with open(file, "r", encoding="utf-8") as f:

        reader = csv.reader(f)

        for row in reader:

            if len(row) >= 3 and row[0] == "info":

                key = row[1]
                value = " | ".join(row[2:])
                if key == "match_id":
                    continue

                if key in match:
                    match[key] += " | " + value
                else:
                    match[key] = value
    all_matches.append(match)

matches = pd.DataFrame(all_matches)

matches.to_csv("matches.csv", index=False)

print("Matches CSV Created!")
print(matches.shape)
print("\nAvailable IPL Seasons:")

seasons = deliveries["season"].dropna().astype(str).unique()

print(sorted(seasons))
print("\nMatches Dataset:")
print(matches[["match_id", "season", "date", "venue", "team", "winner"]].head())
print("\nMatches Columns:")
print(matches.columns.tolist())

print("\nDeliveries Columns:")
print(deliveries.columns.tolist())
print("\nTotal Matches Per Season:")

season_matches = matches.groupby("season")["match_id"].count()

print(season_matches)
print("\nTotal Runs Per Season:")

deliveries["total_runs"] = (
    deliveries["runs_off_bat"] + deliveries["extras"]
)

season_runs = deliveries.groupby("season")["total_runs"].sum()

print(season_runs)

# 1. Top 10 Run Scorers

print("\n1. Top 10 Run Scorers")

top_scorers = deliveries.groupby("striker")["runs_off_bat"].sum()
print(top_scorers.sort_values(ascending=False).head(10))


# 2. Top 10 Wicket Takers

print("\n2. Top 10 Wicket Takers")

wicket_data = deliveries[
    deliveries["wicket_type"].notna()
    & ~deliveries["wicket_type"].isin(["run out", "retired hurt", "obstructing the field", "retired out"])
]

top_wicket_takers = wicket_data.groupby("bowler").size()
print(top_wicket_takers.sort_values(ascending=False).head(10))


# 3. Highest Individual Score

print("\n3. Highest Individual Score")

individual_scores = deliveries.groupby(
    ["match_id", "innings", "striker"]
)["runs_off_bat"].sum()

print(individual_scores.sort_values(ascending=False).head(1))


# 4. Most Successful Teams

print("\n4. Most Successful Teams")

successful_teams = matches["winner"].value_counts()
print(successful_teams.head(10))


# 5. Most Wins by a Team

print("\n5. Most Wins by a Team")

most_wins = matches["winner"].value_counts().head(1)
print(most_wins)

# 6. Toss Decision Analysis

print("\n6. Toss Decision Analysis")

toss_analysis = matches["toss_decision"].value_counts()
print(toss_analysis)


# 7. Player of the Match Analysis

print("\n7. Player of the Match Analysis")

player_awards = matches["player_of_match"].value_counts().head(10)
print(player_awards)


# 8. Batting vs Bowling Performance

print("\n8. Batting vs Bowling Performance")

batting_performance = deliveries.groupby("batting_team")["runs_off_bat"].sum()

bowling_performance = deliveries.groupby("bowling_team")["wicket_type"].count()

print("\nTotal Batting Runs:")
print(batting_performance.sort_values(ascending=False))

print("\nTotal Wickets Taken Against Each Team:")
print(bowling_performance.sort_values(ascending=False))


# 9. Season-wise Run Comparison

print("\n9. Season-wise Run Comparison")

deliveries["total_runs"] = (
    deliveries["runs_off_bat"].fillna(0)
    + deliveries["extras"].fillna(0)
)

season_runs = deliveries.groupby("season")["total_runs"].sum()

print(season_runs.sort_index(key=lambda x: x.astype(str)))

import matplotlib.pyplot as plt
import seaborn as sns

# Top 10 Run Scorers - Improved Bar Chart

plt.figure(figsize=(12, 7))

top_10 = top_scorers.sort_values(ascending=True).tail(10)

sns.barplot(
    x=top_10.values,
    y=top_10.index
)

plt.title("Top 10 IPL Run Scorers", fontsize=16)
plt.xlabel("Total Runs", fontsize=12)
plt.ylabel("Player Names", fontsize=12)

plt.yticks(fontsize=10)
plt.grid(axis="x", linestyle="--", alpha=0.4)

plt.tight_layout()
plt.show()


# Top 10 Wicket Takers - Improved Bar Chart

plt.figure(figsize=(12, 7))

top_10_wickets = top_wicket_takers.sort_values(
    ascending=True
).tail(10)

sns.barplot(
    x=top_10_wickets.values,
    y=top_10_wickets.index
)

plt.title("Top 10 IPL Wicket Takers", fontsize=16)
plt.xlabel("Total Wickets", fontsize=12)
plt.ylabel("Bowler Names", fontsize=12)

plt.yticks(fontsize=10)
plt.grid(axis="x", linestyle="--", alpha=0.4)

plt.tight_layout()
plt.show()



# 3. Season-wise Runs - Line Chart

plt.figure(figsize=(12, 6))

season_runs.plot(kind="line", marker="o")

plt.title("IPL Season-wise Total Runs")
plt.xlabel("Season")
plt.ylabel("Total Runs")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


# 4. Toss Decision - Pie Chart

plt.figure(figsize=(7, 7))

toss_analysis.plot(kind="pie", autopct="%1.1f%%")

plt.title("IPL Toss Decision Analysis")
plt.ylabel("")
plt.tight_layout()
plt.show()

# FINAL IPL DASHBOARD

print("\n" + "=" * 45)
print("          IPL DATA ANALYSIS DASHBOARD")
print("=" * 45)

total_matches = matches["match_id"].nunique()

total_runs = deliveries["runs_off_bat"].sum() + deliveries["extras"].sum()

total_teams = deliveries["batting_team"].nunique()

total_players = deliveries["striker"].nunique()

print("\nTotal Matches:", total_matches)
print("Total Runs:", total_runs)
print("Total Teams:", total_teams)
print("Total Players:", total_players)

print("=" * 45)

# DATA CLEANING AND VALIDATION

print("\n========== DATA QUALITY CHECK ==========")

# 1. Missing Values

print("\nMissing Values in Matches:")
print(matches.isnull().sum())

print("\nMissing Values in Deliveries:")
print(deliveries.isnull().sum())


# 2. Duplicate Records

print("\nDuplicate Records in Matches:")
print(matches.duplicated().sum())

print("\nDuplicate Records in Deliveries:")
print(deliveries.duplicated().sum())


# 3. Dataset Information

print("\nMatches Dataset Information:")
matches.info()

print("\nDeliveries Dataset Information:")
deliveries.info()

print("\n========== CHECK COMPLETED ==========")

# DATA CLEANING SUMMARY

print("\n========== DATA CLEANING SUMMARY ==========")

cleaning_summary = pd.DataFrame({
    "Dataset": ["Matches", "Deliveries"],
    "Total Rows": [len(matches), len(deliveries)],
    "Total Columns": [len(matches.columns), len(deliveries.columns)],
    "Missing Values": [
        matches.isnull().sum().sum(),
        deliveries.isnull().sum().sum()
    ],
    "Duplicate Rows": [
        matches.duplicated().sum(),
        deliveries.duplicated().sum()
    ]
})

print(cleaning_summary)

print("\n========== SUMMARY COMPLETED ==========")

# DATA TYPE VALIDATION

print("\n========== DATA TYPE VALIDATION ==========")

print("\nMatches Data Types:")
print(matches.dtypes)

print("\nDeliveries Data Types:")
print(deliveries.dtypes)

print("\n========== VALIDATION COMPLETED ==========")

# EXPORT ANALYSIS RESULTS

print("\n========== EXPORTING RESULTS ==========")

top_scorers.sort_values(
    ascending=False
).head(10).to_csv("top_10_run_scorers.csv")

top_wicket_takers.sort_values(
    ascending=False
).head(10).to_csv("top_10_wicket_takers.csv")

season_runs.to_csv("season_wise_runs.csv")

successful_teams.to_csv("team_wins.csv")

print("Top Run Scorers CSV Created!")
print("Top Wicket Takers CSV Created!")
print("Season-wise Runs CSV Created!")
print("Team Wins CSV Created!")

print("\n========== EXPORT COMPLETED ==========")
