from fastapi.testclient import TestClient

from app.main import app


# ==========================================
# TEST CLIENT
# ==========================================

client = TestClient(app)


# ==========================================
# HEALTH CHECK TEST
# ==========================================

def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"

    assert data["api"] == (
        "Cricket Analytics API"
    )


# ==========================================
# BASIC API TEST
# ==========================================

def test_cricket():

    response = client.get(
        "/cricket"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == (
        "Cricket Analysis API is running"
    )


# ==========================================
# GET ALL PLAYERS TEST
# ==========================================

def test_get_players():

    response = client.get(
        "/players"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data,
        list
    )

    assert len(data) > 0


# ==========================================
# TOP PLAYERS TEST
# ==========================================

def test_top_players():

    response = client.get(
        "/top-players"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data,
        list
    )

    assert len(data) == 3


# ==========================================
# TOP PLAYERS WITH LIMIT
# ==========================================

def test_top_players_limit():

    response = client.get(
        "/top-players?limit=2"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2


# ==========================================
# PLAYER STATS TEST
# ==========================================

def test_player_stats():

    response = client.get(
        "/player-stats/Virat"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["player"] == "Virat"

    assert "runs" in data

    assert "strike_rate" in data


# ==========================================
# PLAYER NOT FOUND TEST
# ==========================================

def test_player_not_found():

    response = client.get(
        "/player-stats/Unknown"
    )

    assert response.status_code == 404


# ==========================================
# TEAM TEST
# ==========================================

def test_team():

    response = client.get(
        "/team/India"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data,
        list
    )

    assert len(data) > 0


# ==========================================
# TEAM NOT FOUND TEST
# ==========================================

def test_team_not_found():

    response = client.get(
        "/team/Australia"
    )

    assert response.status_code == 404


# ==========================================
# SEARCH PLAYERS TEST
# ==========================================

def test_search_players():

    response = client.get(
        "/players/search?min_runs=50"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data,
        list
    )

    assert len(data) > 0

    for player in data:

        assert player["runs"] >= 50


# ==========================================
# INVALID FILTER TEST
# ==========================================

def test_invalid_filter():

    response = client.get(
        "/players/search"
        "?min_runs=90"
        "&max_runs=40"
    )

    assert response.status_code == 400


# ==========================================
# NO RESULTS TEST
# ==========================================

def test_no_results():

    response = client.get(
        "/players/search?min_runs=1000"
    )

    assert response.status_code == 404


# ==========================================
# PLAYER COMPARISON TEST
# ==========================================

def test_compare_players():

    response = client.get(
        "/compare-players"
        "?player1=Virat"
        "&player2=Root"
    )

    assert response.status_code == 200

    data = response.json()

    assert "player1" in data

    assert "player2" in data


# ==========================================
# PLAYER RATING TEST
# ==========================================

def test_player_rating():

    response = client.get(
        "/player-rating/Virat"
    )

    assert response.status_code == 200

    data = response.json()

    assert "performance_rating" in data

    assert data["player"] == "Virat"


# ==========================================
# ADVANCED TEAM ANALYSIS TEST
# ==========================================

def test_advanced_team_analysis():

    response = client.get(
        "/advanced/team-analysis"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data,
        list
    )

    assert len(data) > 0

    assert "rank" in data[0]


# ==========================================
# ADVANCED RUN ANALYSIS TEST
# ==========================================

def test_advanced_run_analysis():

    response = client.get(
        "/advanced/run-analysis"
    )

    assert response.status_code == 200

    data = response.json()

    assert "mean" in data

    assert "median" in data

    assert "standard_deviation" in data

    assert "percentile_25" in data

    assert "percentile_75" in data

    assert "runs_balls_correlation" in data