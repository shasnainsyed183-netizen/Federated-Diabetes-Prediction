from fastapi import APIRouter, HTTPException
from backend.schemas.prediction_schema import PatientData
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import os

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)

# Paths
MODEL_PATH = "federated_model.h5"
DATA_PATH = "data/cleaned_data.csv"

model = None
scaler = None

# Load model and scaler when the API starts
@router.on_event("startup")
def load_resources():
    global model, scaler
    try:
        # Load the Federated Model
        model = load_model(MODEL_PATH)
        
        # Fit a StandardScaler on the whole dataset for API usage
        df = pd.read_csv(DATA_PATH)
        X = df.drop('readmitted', axis=1)
        scaler = StandardScaler()
        scaler.fit(X)
        
        print("[API] Federated Model and Scaler loaded successfully!")
    except Exception as e:
        print(f"[API] Error loading model: {e}")

@router.post("/")
def predict_readmission(data: PatientData):
    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="Model is not loaded properly.")

    try:
        # Convert Pydantic model to dictionary
        input_dict = data.model_dump(by_alias=True)
        
        # Create a DataFrame with a single row
        input_df = pd.DataFrame([input_dict])
        
        # Ensure the columns are in the exact same order as the training data
        expected_columns = scaler.feature_names_in_
        input_df = input_df[expected_columns]
        
        # Scale the input data
        input_scaled = scaler.transform(input_df)
        
        # Make prediction
        prediction_score = float(model.predict(input_scaled)[0][0])
        
        # Determine result based on threshold
        is_readmitted = prediction_score > 0.5
        result_text = "Patient WILL be readmitted" if is_readmitted else "Patient WILL NOT be readmitted"
        
        return {
            "status": "success",
            "prediction_score": round(prediction_score, 4),
            "prediction": 1 if is_readmitted else 0,
            "message": result_text
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))