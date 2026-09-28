from fastapi import (
    FastAPI,
    Request
)

from fastapi.responses import JSONResponse

import pandas as pd

from app.config import (
    CRICKET_DATA_FILE,
    API_TITLE,
    API_VERSION,
    API_DESCRIPTION,
    ENVIRONMENT
)

from app.routes.players import (
    router as player_router
)

from app.routes.analysis import (
    router as analysis_router
)


# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(
    CRICKET_DATA_FILE
)


# ==========================================
# CREATE APP
# ==========================================

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)


# ==========================================
# PLAYER ROUTES
# ==========================================

app.include_router(
    player_router
)


# ==========================================
# ANALYSIS ROUTES
# ==========================================

app.include_router(
    analysis_router
)


# ==========================================
# GLOBAL EXCEPTION HANDLER
# ==========================================

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": (
                "Something went wrong "
                "while processing the request"
            )
        }
    )


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "api": API_TITLE,
        "version": API_VERSION,
        "environment": ENVIRONMENT,
        "players_loaded": len(df)
    }


# ==========================================
# BASIC API CHECK
# ==========================================

@app.get("/cricket")
def cricket():

    return {
        "message": (
            "Cricket Analysis API is running"
        )
    }