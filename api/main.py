from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import FiniteFloat

BUNDLE_PATH = Path(__file__).resolve().parents[1] / "artifacts/fraud_model.joblib"


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.bundle = joblib.load(BUNDLE_PATH)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/predict")
def predict(transaction: dict[str, FiniteFloat]):
    bundle = app.state.bundle
    features = bundle["features"]
    missing = sorted(set(features) - transaction.keys())
    unexpected = sorted(transaction.keys() - set(features))
    if missing or unexpected:
        raise HTTPException(
            status_code=422,
            detail={"missing": missing, "unexpected": unexpected},
        )

    row = pd.DataFrame([transaction], columns=features)
    score = float(bundle["model"].predict_proba(row)[0, 1])
    threshold = bundle["threshold"]
    decision = "no_policy"
    if threshold is not None:
        decision = "review" if score >= threshold else "allow"

    return {
        "risk_score": score,
        "decision": decision,
        "deployment_approved": False,
    }