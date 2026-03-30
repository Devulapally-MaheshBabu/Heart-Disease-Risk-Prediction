"""
Heart Disease Risk Predictor - FastAPI Backend
Run: uvicorn main:app --reload --port 8000
"""

import pickle
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
import numpy as np

# ─────────────────────────────────────────────
# App Setup
# ─────────────────────────────────────────────
app = FastAPI(
    title="Heart Disease Risk Predictor API",
    description="Predicts heart disease risk using a trained Random Forest model.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "https://heart-disease-risk-prediction-self.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# Load Model on Startup
# ─────────────────────────────────────────────
MODEL_PATH = Path(__file__).parent.parent / "ml" / "model.pkl"
META_PATH  = Path(__file__).parent.parent / "ml" / "model_metadata.json"

model = None
metadata = {}

@app.on_event("startup")
def load_model():
    global model, metadata
    if not MODEL_PATH.exists():
        raise RuntimeError(f"Model not found at {MODEL_PATH}. Run ml/train_model.py first.")
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    if META_PATH.exists():
        with open(META_PATH) as f:
            metadata = json.load(f)
    print(f"✅ Model loaded | Accuracy: {metadata.get('accuracy', 'N/A')}")

# ─────────────────────────────────────────────
# Input Schema (Pydantic)
# ─────────────────────────────────────────────
class PatientData(BaseModel):
    age:      float = Field(..., ge=20, le=100,  description="Age in years (20–100)")
    sex:      float = Field(..., ge=0,  le=1,    description="Sex: 0=Female, 1=Male")
    cp:       float = Field(..., ge=0,  le=3,    description="Chest pain type (0–3)")
    trestbps: float = Field(..., ge=80, le=220,  description="Resting blood pressure (mmHg)")
    chol:     float = Field(..., ge=100, le=600, description="Serum cholesterol (mg/dl)")
    fbs:      float = Field(..., ge=0,  le=1,    description="Fasting blood sugar >120 mg/dl: 0=No, 1=Yes")
    restecg:  float = Field(..., ge=0,  le=2,    description="Resting ECG results (0–2)")
    thalach:  float = Field(..., ge=60, le=220,  description="Max heart rate achieved")
    exang:    float = Field(..., ge=0,  le=1,    description="Exercise-induced angina: 0=No, 1=Yes")
    oldpeak:  float = Field(..., ge=0,  le=7,    description="ST depression induced by exercise")
    slope:    float = Field(..., ge=0,  le=2,    description="Slope of peak exercise ST segment (0–2)")
    ca:       float = Field(..., ge=0,  le=3,    description="Number of major vessels colored by fluoroscopy (0–3)")
    thal:     float = Field(..., ge=0,  le=3,    description="Thalassemia: 0=Normal, 1=Fixed defect, 2=Reversible defect, 3=Unknown")

    @field_validator("age", "trestbps", "chol", "thalach")
    @classmethod
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Value must be positive")
        return v

    model_config = {"json_schema_extra": {
        "example": {
            "age": 54, "sex": 1, "cp": 2, "trestbps": 130, "chol": 245,
            "fbs": 0, "restecg": 1, "thalach": 162, "exang": 0,
            "oldpeak": 0.0, "slope": 2, "ca": 0, "thal": 2
        }
    }}

# ─────────────────────────────────────────────
# Response Schema
# ─────────────────────────────────────────────
class PredictionResponse(BaseModel):
    prediction:   int
    label:        str
    probability:  float
    risk_level:   str
    message:      str

# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "status": "running",
        "model": metadata.get("model_type", "unknown"),
        "accuracy": metadata.get("accuracy"),
        "docs": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict", response_model=PredictionResponse)
def predict(data: PatientData):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded.")

    features = np.array([[
        data.age, data.sex, data.cp, data.trestbps, data.chol,
        data.fbs, data.restecg, data.thalach, data.exang,
        data.oldpeak, data.slope, data.ca, data.thal
    ]])

    prediction  = int(model.predict(features)[0])
    probability = round(float(model.predict_proba(features)[0][1]), 4)

    if probability < 0.35:
        risk_level = "Low"
        message = "Low risk indicators detected. Maintain a healthy lifestyle."
    elif probability < 0.65:
        risk_level = "Moderate"
        message = "Moderate risk detected. Consult a physician for further evaluation."
    else:
        risk_level = "High"
        message = "High risk indicators detected. Please seek medical attention promptly."

    return PredictionResponse(
        prediction=prediction,
        label="Disease Detected" if prediction == 1 else "No Disease Detected",
        probability=probability,
        risk_level=risk_level,
        message=message
    )

@app.get("/model-info")
def model_info():
    return metadata