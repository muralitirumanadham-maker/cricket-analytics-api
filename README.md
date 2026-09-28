# 🏏 Cricket Analytics API

A medium-level REST API built with **Python, Pandas, NumPy, FastAPI, and Pydantic** for analyzing cricket player and team statistics.

This project was created as a practical revision project to combine data analysis and backend API development.

---

## 🚀 Features

### Player Analysis
- Get all players
- Get player details
- Search and filter players
- Get top players
- Get individual player statistics
- Compare two players
- Calculate player performance rating

### Team Analysis
- Get team players
- Get team top scorers
- Analyze team statistics
- Advanced team analysis

### Cricket Analytics
- Total runs
- Average runs
- Highest and lowest runs
- Standard deviation
- Players scoring above 50
- Strike rate
- Boundary percentage
- Bowling statistics
- Run analysis
- Player performance rating

### File Analysis
- Upload CSV files
- Validate uploaded CSV files
- Analyze uploaded run data
- Detect missing values
- Display data types and column information

### API Features
- FastAPI REST endpoints
- Swagger API documentation
- Pydantic request validation
- Pydantic response models
- HTTP error handling
- Global exception handling
- Health check endpoint
- Environment configuration
- Automated API testing with Pytest

---

## 🛠️ Technologies Used

- Python
- NumPy
- Pandas
- FastAPI
- Pydantic
- Uvicorn
- Pytest
- HTTPX
- python-dotenv

---

## 📁 Project Structure

```text
cricket-analytics-api/
│
├── .gitignore
├── requirements.txt
├── README.md
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   │
│   ├── data/
│   │   └── cricket.csv
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── players.py
│   │   └── analysis.py
│   │
│   └── services/
│       ├── __init__.py
│       └── analytics.py
│
└── tests/
    ├── __init__.py
    └── test_api.py
