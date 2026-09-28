import io

import pandas as pd
import numpy as np

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from pydantic import BaseModel, Field

from app.config import CRICKET_DATA_FILE

from app.services.analytics import (
    analyze_runs,
    analyze_teams,
    advanced_team_analysis,
    advanced_run_analysis
)


router = APIRouter()


# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(
    CRICKET_DATA_FILE
)


# ==========================================
# PLAYER INNINGS MODEL
# ==========================================

class Innings(BaseModel):

    player: str

    runs: int = Field(
        ge=0
    )

    balls: int = Field(
        gt=0
    )

    fours: int = Field(
        ge=0
    )

    sixes: int = Field(
        ge=0
    )


# ==========================================
# ANALYZE PLAYER
# ==========================================

@router.post("/analyze")
def analyze(data: Innings):

    strike_rate = (
        data.runs / data.balls
    ) * 100

    boundary_runs = (
        data.fours * 4
    ) + (
        data.sixes * 6
    )

    boundary_percentage = 0

    if data.runs > 0:

        boundary_percentage = (
            boundary_runs / data.runs
        ) * 100

    return {
        "player": data.player,
        "runs": data.runs,
        "balls": data.balls,
        "strike_rate": round(
            strike_rate,
            2
        ),
        "boundary_runs": boundary_runs,
        "boundary_percentage": round(
            boundary_percentage,
            2
        )
    }


# ==========================================
# UPLOAD CSV
# ==========================================

@router.post("/upload")
def upload(
    file: UploadFile = File(...)
):

    contents = file.file.read()

    try:

        uploaded_df = pd.read_csv(
            io.BytesIO(contents)
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid CSV file"
        )

    rows, columns = uploaded_df.shape

    return {
        "filename": file.filename,
        "rows": rows,
        "columns": columns,
        "column_names":
            uploaded_df.columns.tolist(),
        "missing_values":
            uploaded_df.isnull()
            .sum()
            .to_dict(),
        "data_types":
            uploaded_df.dtypes
            .astype(str)
            .to_dict()
    }


# ==========================================
# ANALYZE UPLOADED CSV
# ==========================================

@router.post("/analyze-file")
def analyze_file(
    file: UploadFile = File(...)
):

    contents = file.file.read()

    try:

        uploaded_df = pd.read_csv(
            io.BytesIO(contents)
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid CSV file"
        )

    if "runs" not in uploaded_df.columns:

        raise HTTPException(
            status_code=400,
            detail="CSV must contain a 'runs' column"
        )

    runs = pd.to_numeric(
        uploaded_df["runs"],
        errors="coerce"
    )

    runs = runs.dropna()

    if len(runs) == 0:

        raise HTTPException(
            status_code=400,
            detail=(
                "Runs column contains "
                "no valid numeric values"
            )
        )

    runs_array = np.array(
        runs
    )

    results = analyze_runs(
        runs_array
    )

    return {
        "filename": file.filename,
        **results
    }


# ==========================================
# TEAM ANALYSIS
# ==========================================

@router.get("/teams")
def teams():

    return analyze_teams(
        df
    )


# ==========================================
# ADVANCED TEAM ANALYSIS
# ==========================================

@router.get(
    "/advanced/team-analysis"
)
def advanced_teams():

    return advanced_team_analysis(
        df
    )


# ==========================================
# ADVANCED RUN ANALYSIS
# ==========================================

@router.get(
    "/advanced/run-analysis"
)
def advanced_runs():

    return advanced_run_analysis(
        df
    )