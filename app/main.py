from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


app = FastAPI(
    title="FraudShield API",
    description="AI-powered PaySim transaction fraud detection API",
    version="1.0.0"
)


# -------------------------
# Frontend
# -------------------------

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


# -------------------------
# Load Model
# -------------------------

pipeline = joblib.load(
    "models/fraud_paysim_pipeline.pkl"
)

threshold = joblib.load(
    "models/fraud_paysim_threshold.pkl"
)


# -------------------------
# Request Schema
# -------------------------

class Transaction(BaseModel):

    step: int = Field(
        ...,
        ge=1,
        description="Transaction time step (1 step = 1 hour)"
    )

    type: str = Field(
        ...,
        description="Transaction type"
    )

    amount: float = Field(
        ...,
        gt=0,
        description="Transaction amount"
    )

    oldbalanceOrg: float = Field(
        ...,
        ge=0,
        description="Sender's previous balance"
    )

    oldbalanceDest: float = Field(
        ...,
        ge=0,
        description="Receiver's previous balance"
    )


# -------------------------
# Allowed Transaction Types
# -------------------------

ALLOWED_TYPES = {
    "PAYMENT",
    "TRANSFER",
    "CASH_OUT",
    "CASH_IN",
    "DEBIT"
}


# -------------------------
# Home
# -------------------------

@app.get("/")
def home():
    return FileResponse(
        "app/static/index.html"
    )


# -------------------------
# Health Check
# -------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": "PaySim XGBoost",
        "threshold": round(float(threshold), 4)
    }


# -------------------------
# Fraud Prediction
# -------------------------

@app.post("/predict")
def predict(transaction: Transaction):

    # Validate transaction type
    if transaction.type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid transaction type. Allowed types: {sorted(ALLOWED_TYPES)}"
        )

    try:

        # Convert request to DataFrame
        data = pd.DataFrame([transaction.model_dump()])

        # Get fraud probability
        probability = pipeline.predict_proba(data)[0][1]

        # Apply tuned threshold
        prediction = int(
            probability >= threshold
        )

        # Result
        result = (
            "Fraud"
            if prediction == 1
            else "Legitimate"
        )

        return {
            "prediction": prediction,
            "result": result,
            "fraud_probability": round(
                float(probability),
                4
            ),
            "threshold": round(
                float(threshold),
                4
            )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )