from pathlib import Path

import os

from dotenv import load_dotenv


# ==========================================
# PROJECT PATH
# ==========================================

BASE_DIR = Path(
    __file__
).resolve().parent


# ==========================================
# PROJECT ROOT
# ==========================================

PROJECT_ROOT = BASE_DIR.parent


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(
    ENV_FILE
)


# ==========================================
# DATA PATH
# ==========================================

DATA_DIR = BASE_DIR / "data"

CRICKET_DATA_FILE = (
    DATA_DIR / "cricket.csv"
)


# ==========================================
# API CONFIGURATION
# ==========================================

API_TITLE = os.getenv(
    "API_TITLE",
    "Cricket Analytics API"
)


API_VERSION = os.getenv(
    "API_VERSION",
    "1.0.0"
)


API_DESCRIPTION = os.getenv(
    "API_DESCRIPTION",
    "API for Cricket Player and Team Analytics"
)


# ==========================================
# ENVIRONMENT
# ==========================================

ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development"
)