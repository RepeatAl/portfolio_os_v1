from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uuid

from engines.engine_runner import run_all_engines

app = FastAPI()

# =========================
# IN-MEMORY DATABASE
# =========================

users = {}
portfolios = {}

# =========================
# MODELS
# =========================

class UserCreate(BaseModel):
    email: str


class Asset(BaseModel):
    ticker: str
    quantity: float
    category: str


class PortfolioUpdate(BaseModel):
    assets: List[Asset]


# =========================
# USER
# =========================

@app.post("/create_user")
def create_user(user: UserCreate):

    user_id = str(uuid.uuid4())

    users[user_id] = {
        "email": user.email
    }

    portfolios[user_id] = []

    return {
        "user_id": user_id,
        "email": user.email
    }


# =========================
# PORTFOLIO
# =========================

@app.post("/update_portfolio/{user_id}")
def update_portfolio(user_id: str, data: PortfolioUpdate):

    portfolios[user_id] = [asset.dict() for asset in data.assets]

    return {
        "message": "Portfolio updated",
        "assets": portfolios[user_id]
    }


@app.get("/get_portfolio/{user_id}")
def get_portfolio(user_id: str):

    return {
        "portfolio": portfolios.get(user_id, [])
    }


# =========================
# ANALYSIS
# =========================

@app.get("/run_analysis/{user_id}")
def run_analysis(user_id: str):

    user_portfolio = portfolios.get(user_id, [])

    results = run_all_engines(user_portfolio)

    return results