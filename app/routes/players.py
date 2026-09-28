import pandas as pd

from fastapi import (
    APIRouter,
    Query,
    HTTPException
)

from pydantic import BaseModel

from app.config import CRICKET_DATA_FILE

from app.services.analytics import (
    get_top_players,
    get_player_stats,
    get_team_players,
    get_team_top_scorers,
    compare_players,
    get_bowling_stats,
    get_player_rating
)


router = APIRouter()


# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(
    CRICKET_DATA_FILE
)


# ==========================================
# RESPONSE MODELS
# ==========================================

class PlayerBasicResponse(BaseModel):

    player: str
    team: str
    runs: int


class PlayerSearchResponse(BaseModel):

    player: str
    team: str
    runs: int
    sixes: int


class PlayerDetailResponse(BaseModel):

    player: str
    team: str
    runs: int
    balls: int
    fours: int
    sixes: int
    wickets: int
    overs: int


class PlayerStatsResponse(BaseModel):

    player: str
    team: str
    runs: int
    balls: int
    fours: int
    sixes: int
    strike_rate: float


class TopPlayerResponse(BaseModel):

    player: str
    runs: int


class TeamPlayerResponse(BaseModel):

    player: str
    team: str
    runs: int


class ComparedPlayer(BaseModel):

    player: str
    team: str
    runs: int
    balls: int
    fours: int
    sixes: int
    strike_rate: float


class PlayerComparisonResponse(BaseModel):

    player1: ComparedPlayer
    player2: ComparedPlayer


class BowlingStatsResponse(BaseModel):

    player: str
    team: str
    overs: float
    runs: int
    wickets: int
    economy_rate: float
    wickets_per_over: float


class PlayerRatingResponse(BaseModel):

    player: str
    team: str
    runs: int
    strike_rate: float
    fours: int
    sixes: int
    wickets: int
    performance_rating: float


# ==========================================
# GET ALL PLAYERS
# ==========================================

@router.get(
    "/players",
    response_model=list[PlayerBasicResponse]
)
def players():

    selected_df = df[
        ["player", "team", "runs"]
    ]

    return selected_df.to_dict(
        orient="records"
    )


# ==========================================
# ADVANCED PLAYER SEARCH
# ==========================================

@router.get(
    "/players/search",
    response_model=list[PlayerSearchResponse]
)
def search_players(

    team: str | None = None,

    min_runs: int | None = Query(
        default=None,
        ge=0
    ),

    max_runs: int | None = Query(
        default=None,
        ge=0
    ),

    min_sixes: int | None = Query(
        default=None,
        ge=0
    )
):

    if (
        min_runs is not None
        and max_runs is not None
        and min_runs > max_runs
    ):

        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid filter range",
                "message": (
                    "min_runs cannot be greater "
                    "than max_runs"
                )
            }
        )

    filtered_df = df.copy()

    if team is not None:

        filtered_df = filtered_df[
            filtered_df["team"].str.lower()
            == team.lower()
        ]

    if min_runs is not None:

        filtered_df = filtered_df[
            filtered_df["runs"] >= min_runs
        ]

    if max_runs is not None:

        filtered_df = filtered_df[
            filtered_df["runs"] <= max_runs
        ]

    if min_sixes is not None:

        filtered_df = filtered_df[
            filtered_df["sixes"] >= min_sixes
        ]

    if filtered_df.empty:

        raise HTTPException(
            status_code=404,
            detail={
                "error": "No results",
                "message": (
                    "No players match "
                    "the given filters"
                )
            }
        )

    return filtered_df[
        [
            "player",
            "team",
            "runs",
            "sixes"
        ]
    ].to_dict(
        orient="records"
    )


# ==========================================
# GET PLAYER BY NAME
# ==========================================

@router.get(
    "/player/{player_name}",
    response_model=PlayerDetailResponse
)
def player(player_name: str):

    player_df = df[
        df["player"].str.lower()
        == player_name.lower()
    ]

    if player_df.empty:

        raise HTTPException(
            status_code=404,
            detail={
                "error": "Player not found",
                "message": (
                    f"No player found "
                    f"with name '{player_name}'"
                )
            }
        )

    row = player_df.iloc[0]

    return {
        "player": row["player"],
        "team": row["team"],
        "runs": int(row["runs"]),
        "balls": int(row["balls"]),
        "fours": int(row["fours"]),
        "sixes": int(row["sixes"]),
        "wickets": int(row["wickets"]),
        "overs": int(row["overs"])
    }


# ==========================================
# FILTER PLAYERS
# ==========================================

@router.get(
    "/player/filter",
    response_model=list[PlayerBasicResponse]
)
def filter_players(

    min_runs: int = Query(
        default=0,
        ge=0
    )
):

    filtered_df = df[
        df["runs"] >= min_runs
    ]

    return filtered_df[
        ["player", "team", "runs"]
    ].to_dict(
        orient="records"
    )


# ==========================================
# TOP PLAYERS
# ==========================================

@router.get(
    "/top-players",
    response_model=list[TopPlayerResponse]
)
def top_players(

    limit: int = Query(
        default=3,
        ge=1,
        le=20
    )
):

    return get_top_players(
        df,
        limit
    )


# ==========================================
# PLAYER STATISTICS
# ==========================================

@router.get(
    "/player-stats/{player_name}",
    response_model=PlayerStatsResponse
)
def player_stats(player_name: str):

    result = get_player_stats(
        df,
        player_name
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail={
                "error": "Player not found",
                "message": (
                    f"No statistics found "
                    f"for '{player_name}'"
                )
            }
        )

    return result


# ==========================================
# TEAM PLAYERS
# ==========================================

@router.get(
    "/team/{team_name}",
    response_model=list[TeamPlayerResponse]
)
def team_players(team_name: str):

    result = get_team_players(
        df,
        team_name
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail={
                "error": "Team not found",
                "message": (
                    f"No team found "
                    f"with name '{team_name}'"
                )
            }
        )

    return result


# ==========================================
# TEAM TOP SCORERS
# ==========================================

@router.get(
    "/team/{team_name}/top-scorers",
    response_model=list[TeamPlayerResponse]
)
def team_top_scorers(

    team_name: str,

    limit: int = Query(
        default=3,
        ge=1,
        le=20
    )
):

    result = get_team_top_scorers(
        df,
        team_name,
        limit
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail={
                "error": "Team not found",
                "message": (
                    f"No team found "
                    f"with name '{team_name}'"
                )
            }
        )

    return result


# ==========================================
# COMPARE TWO PLAYERS
# ==========================================

@router.get(
    "/compare-players",
    response_model=PlayerComparisonResponse
)
def compare_two_players(
    player1: str,
    player2: str
):

    result = compare_players(
        df,
        player1,
        player2
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail={
                "error": "Player comparison failed",
                "message": (
                    "One or both players "
                    "were not found"
                )
            }
        )

    return result


# ==========================================
# BOWLING STATISTICS
# ==========================================

@router.get(
    "/bowling-stats/{player_name}",
    response_model=BowlingStatsResponse
)
def bowling_stats(player_name: str):

    result = get_bowling_stats(
        df,
        player_name
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail={
                "error": "Player not found",
                "message": (
                    f"No bowling statistics "
                    f"found for '{player_name}'"
                )
            }
        )

    return result


# ==========================================
# PLAYER PERFORMANCE RATING
# ==========================================

@router.get(
    "/player-rating/{player_name}",
    response_model=PlayerRatingResponse
)
def player_rating(player_name: str):

    result = get_player_rating(
        df,
        player_name
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail={
                "error": "Player not found",
                "message": (
                    f"No performance rating "
                    f"found for '{player_name}'"
                )
            }
        )

    return result