import numpy as np
import pandas as pd


# ==========================================
# RUN ANALYSIS
# ==========================================

def analyze_runs(runs_array):

    runs_array = np.array(runs_array)

    return {
        "total_runs": int(np.sum(runs_array)),
        "average_runs": float(np.mean(runs_array)),
        "highest_runs": int(np.max(runs_array)),
        "lowest_runs": int(np.min(runs_array)),
        "standard_deviation": float(np.std(runs_array)),
        "players_above_50": int(np.sum(runs_array > 50))
    }


# ==========================================
# TEAM ANALYSIS
# ==========================================

def analyze_teams(df):

    results = []

    for team, group in df.groupby("team"):

        results.append({
            "team": team,
            "total_runs": int(group["runs"].sum()),
            "avg_runs": float(group["runs"].mean()),
            "max_runs": int(group["runs"].max()),
            "total_wickets": int(group["wickets"].sum())
        })

    return results


# ==========================================
# TOP PLAYERS
# ==========================================

def get_top_players(df, limit=3):

    top_players = (
        df.sort_values(
            "runs",
            ascending=False
        )
        .head(limit)
    )

    return top_players[
        ["player", "runs"]
    ].to_dict(
        orient="records"
    )


# ==========================================
# PLAYER STATISTICS
# ==========================================

def get_player_stats(df, player_name):

    player_df = df[
        df["player"].str.lower()
        == player_name.lower()
    ]

    if player_df.empty:
        return None

    row = player_df.iloc[0]

    strike_rate = (
        row["runs"] / row["balls"]
    ) * 100

    return {
        "player": row["player"],
        "team": row["team"],
        "runs": int(row["runs"]),
        "balls": int(row["balls"]),
        "fours": int(row["fours"]),
        "sixes": int(row["sixes"]),
        "strike_rate": round(
            float(strike_rate),
            2
        )
    }


# ==========================================
# TEAM PLAYERS
# ==========================================

def get_team_players(df, team_name):

    team_df = df[
        df["team"].str.lower()
        == team_name.lower()
    ]

    if team_df.empty:
        return None

    return team_df[
        ["player", "team", "runs"]
    ].to_dict(
        orient="records"
    )


# ==========================================
# TEAM TOP SCORERS
# ==========================================

def get_team_top_scorers(
    df,
    team_name,
    limit=3
):

    team_df = df[
        df["team"].str.lower()
        == team_name.lower()
    ]

    if team_df.empty:
        return None

    top_scorers = (
        team_df
        .sort_values(
            "runs",
            ascending=False
        )
        .head(limit)
    )

    return top_scorers[
        ["player", "team", "runs"]
    ].to_dict(
        orient="records"
    )


# ==========================================
# PLAYER COMPARISON
# ==========================================

def compare_players(
    df,
    player1,
    player2
):

    player1_df = df[
        df["player"].str.lower()
        == player1.lower()
    ]

    player2_df = df[
        df["player"].str.lower()
        == player2.lower()
    ]

    if player1_df.empty or player2_df.empty:
        return None

    p1 = player1_df.iloc[0]
    p2 = player2_df.iloc[0]

    p1_strike_rate = (
        p1["runs"] / p1["balls"]
    ) * 100

    p2_strike_rate = (
        p2["runs"] / p2["balls"]
    ) * 100

    return {
        "player1": {
            "player": p1["player"],
            "team": p1["team"],
            "runs": int(p1["runs"]),
            "balls": int(p1["balls"]),
            "fours": int(p1["fours"]),
            "sixes": int(p1["sixes"]),
            "strike_rate": round(
                float(p1_strike_rate),
                2
            )
        },

        "player2": {
            "player": p2["player"],
            "team": p2["team"],
            "runs": int(p2["runs"]),
            "balls": int(p2["balls"]),
            "fours": int(p2["fours"]),
            "sixes": int(p2["sixes"]),
            "strike_rate": round(
                float(p2_strike_rate),
                2
            )
        }
    }


# ==========================================
# BOWLING STATISTICS
# ==========================================

def get_bowling_stats(
    df,
    player_name
):

    player_df = df[
        df["player"].str.lower()
        == player_name.lower()
    ]

    if player_df.empty:
        return None

    row = player_df.iloc[0]

    overs = float(row["overs"])
    wickets = int(row["wickets"])
    runs = int(row["runs"])

    if overs > 0:

        economy_rate = runs / overs
        wickets_per_over = wickets / overs

    else:

        economy_rate = 0
        wickets_per_over = 0

    return {
        "player": row["player"],
        "team": row["team"],
        "overs": overs,
        "runs": runs,
        "wickets": wickets,
        "economy_rate": round(
            economy_rate,
            2
        ),
        "wickets_per_over": round(
            wickets_per_over,
            2
        )
    }


# ==========================================
# PLAYER PERFORMANCE RATING
# ==========================================

def get_player_rating(
    df,
    player_name
):

    player_df = df[
        df["player"].str.lower()
        == player_name.lower()
    ]

    if player_df.empty:
        return None

    row = player_df.iloc[0]

    runs = float(row["runs"])
    balls = float(row["balls"])
    fours = float(row["fours"])
    sixes = float(row["sixes"])
    wickets = float(row["wickets"])

    if balls > 0:

        strike_rate = (
            runs / balls
        ) * 100

    else:

        strike_rate = 0

    rating = (
        (runs * 0.5)
        + (strike_rate * 0.2)
        + (fours * 1)
        + (sixes * 2)
        + (wickets * 5)
    )

    return {
        "player": row["player"],
        "team": row["team"],
        "runs": int(runs),
        "strike_rate": round(
            strike_rate,
            2
        ),
        "fours": int(fours),
        "sixes": int(sixes),
        "wickets": int(wickets),
        "performance_rating": round(
            rating,
            2
        )
    }


# ==========================================
# ADVANCED TEAM ANALYSIS
# STEP 16
# ==========================================

def advanced_team_analysis(df):

    team_stats = (
        df.groupby("team")
        .agg(
            total_runs=("runs", "sum"),
            average_runs=("runs", "mean"),
            highest_runs=("runs", "max"),
            lowest_runs=("runs", "min"),
            total_wickets=("wickets", "sum"),
            players=("player", "count")
        )
        .reset_index()
    )

    team_stats["average_runs"] = (
        team_stats["average_runs"]
        .round(2)
    )

    team_stats["rank"] = (
        team_stats["total_runs"]
        .rank(
            ascending=False,
            method="dense"
        )
        .astype(int)
    )

    team_stats = team_stats.sort_values(
        "rank"
    )

    return team_stats.to_dict(
        orient="records"
    )


# ==========================================
# ADVANCED NUMPY RUN ANALYSIS
# STEP 17
# ==========================================

def advanced_run_analysis(df):

    runs = np.array(
        df["runs"],
        dtype=float
    )

    balls = np.array(
        df["balls"],
        dtype=float
    )

    correlation = np.corrcoef(
        runs,
        balls
    )[0, 1]

    return {
        "mean": round(
            float(np.mean(runs)),
            2
        ),
        "median": round(
            float(np.median(runs)),
            2
        ),
        "standard_deviation": round(
            float(np.std(runs)),
            2
        ),
        "percentile_25": round(
            float(np.percentile(runs, 25)),
            2
        ),
        "percentile_50": round(
            float(np.percentile(runs, 50)),
            2
        ),
        "percentile_75": round(
            float(np.percentile(runs, 75)),
            2
        ),
        "runs_balls_correlation": round(
            float(correlation),
            2
        )
    }