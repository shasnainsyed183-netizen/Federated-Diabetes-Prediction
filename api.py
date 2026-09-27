# api.py
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pandas as pd
import pickle
import tensorflow as tf

app = FastAPI(
    title="MediFederate REST API",
    description="Production-grade API for MediFederate Multi-Disease Prediction Platform",
    version="1.0.0"
)

# ========================================
# LOAD ALL MODELS
# ========================================
print("Loading Models...")

# Diabetes
diabetes_model = tf.keras.models.load_model('federated_dp_model.keras')
diabetes_scaler = pickle.load(open('scaler.pkl', 'rb'))
diabetes_features = pickle.load(open('feature_names.pkl', 'rb'))

# Heart Disease
heart_model = tf.keras.models.load_model('heart_dp_model.keras')
heart_scaler = pickle.load(open('scaler_heart.pkl', 'rb'))
heart_features = pickle.load(open('feature_names_heart.pkl', 'rb'))

# Stroke
stroke_model = tf.keras.models.load_model('stroke_dp_model.keras')
stroke_scaler = pickle.load(open('scaler_stroke.pkl', 'rb'))
stroke_features = pickle.load(open('feature_names_stroke.pkl', 'rb'))

# Kidney Disease
kidney_model = tf.keras.models.load_model('kidney_dp_model.keras')
kidney_scaler = pickle.load(open('scaler_kidney.pkl', 'rb'))
kidney_features = pickle.load(open('feature_names_kidney.pkl', 'rb'))

# Thyroid
thyroid_model = tf.keras.models.load_model('thyroid_dp_model.keras')
thyroid_scaler = pickle.load(open('scaler_thyroid.pkl', 'rb'))
thyroid_features = [
    'age', 'sex', 'TSH', 'T3', 'TT4', 'T4U', 'FTI', 
    'on_thyroxine', 'query_on_thyroxine', 'on_antithyroid_meds', 
    'sick', 'pregnant', 'thyroid_surgery', 'I131_treatment', 
    'query_hypothyroid', 'query_hyperthyroid', 'lithium', 
    'goitre', 'tumor', 'hypopituitary', 'psych', 
    'TSH_measured', 'T3_measured', 'TT4_measured', 
    'T4U_measured', 'FTI_measured', 'TBG_measured'
]

print("All Models Loaded Successfully!")

# ========================================
# PYDANTIC SCHEMAS
# ========================================
class DiabetesInput(BaseModel):
    age: int
    time_in_hospital: int
    num_medications: int
    num_lab_procedures: int
    number_diagnoses: int
    num_procedures: int
    number_inpatient: int
    number_emergency: int

class HeartInput(BaseModel):
    age: int
    sex: int  # 1: Male, 0: Female
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

class StrokeInput(BaseModel):
    gender: int  # 1: Male, 0: Female
    age: int
    hypertension: int
    heart_disease: int
    ever_married: int
    Residence_type: int
    avg_glucose_level: float
    bmi: float
    smoking_status: int
    work_type_Never_worked: int
    work_type_Private: int
    work_type_Self_employed: int
    work_type_children: int

class KidneyInput(BaseModel):
    age: int
    bp: int
    sg: float
    al: int
    su: int
    bgr: int
    bu: int
    sc: float
    sod: int
    pot: float
    hemo: float
    pcv: int
    wc: int
    rc: float
    htn: int
    dm: int
    cad: int
    appet: int
    pe: int
    ane: int
    rbc: int
    pc: int
    pcc: int
    ba: int

class ThyroidInput(BaseModel):
    age: int
    sex: int
    TSH: float
    T3: float
    TT4: float
    T4U: float
    FTI: float
    on_thyroxine: int
    query_on_thyroxine: int
    on_antithyroid_meds: int
    sick: int
    pregnant: int
    thyroid_surgery: int
    I131_treatment: int
    query_hypothyroid: int
    query_hyperthyroid: int
    lithium: int
    goitre: int
    tumor: int
    hypopituitary: int
    psych: int
    TSH_measured: int
    T3_measured: int
    TT4_measured: int
    T4U_measured: int
    FTI_measured: int
    TBG_measured: int

# ========================================
# HELPER FUNCTION
# ========================================
def predict_disease(model, scaler, features, data_dict):
    input_df = pd.DataFrame(np.zeros((1, len(features))), columns=features)
    for key, val in data_dict.items():
        if key in input_df.columns:
            input_df[key] = val
    input_scaled = scaler.transform(input_df)
    probability = float(model.predict(input_scaled, verbose=0)[0][0])
    return probability

# ========================================
# API ENDPOINTS
# ========================================
@app.get("/")
def read_root():
    return {"message": "Welcome to MediFederate REST API", "status": "Active"}

@app.post("/predict/diabetes")
def predict_diabetes(data: DiabetesInput):
    prob = predict_disease(
        diabetes_model, diabetes_scaler, diabetes_features,
        {
            'age': data.age, 'time_in_hospital': data.time_in_hospital,
            'num_medications': data.num_medications, 'num_lab_procedures': data.num_lab_procedures,
            'number_diagnoses': data.number_diagnoses, 'num_procedures': data.num_procedures,
            'number_inpatient': data.number_inpatient, 'number_emergency': data.number_emergency
        }
    )
    return {
        "disease": "Diabetes",
        "probability": round(prob * 100, 2),
        "risk_level": "High Risk" if prob > 0.5 else "Low Risk",
        "data_shared": "0 bytes",
        "privacy": "Differential Privacy Enabled"
    }

@app.post("/predict/heart")
def predict_heart(data: HeartInput):
    prob = predict_disease(
        heart_model, heart_scaler, heart_features,
        {
            'age': data.age, 'sex': data.sex, 'cp': data.cp,
            'trestbps': data.trestbps, 'chol': data.chol, 'fbs': data.fbs,
            'restecg': data.restecg, 'thalach': data.thalach, 'exang': data.exang,
            'oldpeak': data.oldpeak, 'slope': data.slope, 'ca': data.ca, 'thal': data.thal
        }
    )
    return {
        "disease": "Heart Disease",
        "probability": round(prob * 100, 2),
        "risk_level": "High Risk" if prob > 0.5 else "Low Risk",
        "data_shared": "0 bytes",
        "privacy": "Differential Privacy Enabled"
    }

@app.post("/predict/stroke")
def predict_stroke(data: StrokeInput):
    prob = predict_disease(
        stroke_model, stroke_scaler, stroke_features,
        {
            'gender': data.gender, 'age': data.age, 'hypertension': data.hypertension,
            'heart_disease': data.heart_disease, 'ever_married': data.ever_married,
            'Residence_type': data.Residence_type, 'avg_glucose_level': data.avg_glucose_level,
            'bmi': data.bmi, 'smoking_status': data.smoking_status,
            'work_type_Never_worked': data.work_type_Never_worked,
            'work_type_Private': data.work_type_Private,
            'work_type_Self-employed': data.work_type_Self_employed,
            'work_type_children': data.work_type_children
        }
    )
    return {
        "disease": "Stroke",
        "probability": round(prob * 100, 2),
        "risk_level": "High Risk" if prob > 0.5 else "Low Risk",
        "data_shared": "0 bytes",
        "privacy": "Differential Privacy Enabled"
    }

@app.post("/predict/kidney")
def predict_kidney(data: KidneyInput):
    prob = predict_disease(
        kidney_model, kidney_scaler, kidney_features,
        {
            'age': data.age, 'bp': data.bp, 'sg': data.sg, 'al': data.al,
            'su': data.su, 'bgr': data.bgr, 'bu': data.bu, 'sc': data.sc,
            'sod': data.sod, 'pot': data.pot, 'hemo': data.hemo, 'pcv': data.pcv,
            'wc': data.wc, 'rc': data.rc, 'htn': data.htn, 'dm': data.dm,
            'cad': data.cad, 'appet': data.appet, 'pe': data.pe, 'ane': data.ane,
            'rbc': data.rbc, 'pc': data.pc, 'pcc': data.pcc, 'ba': data.ba
        }
    )
    return {
        "disease": "Kidney Disease",
        "probability": round(prob * 100, 2),
        "risk_level": "High Risk" if prob > 0.5 else "Low Risk",
        "data_shared": "0 bytes",
        "privacy": "Differential Privacy Enabled"
    }

@app.post("/predict/thyroid")
def predict_thyroid(data: ThyroidInput):
    prob = predict_disease(
        thyroid_model, thyroid_scaler, thyroid_features,
        {
            'age': data.age, 'sex': data.sex, 'TSH': data.TSH, 'T3': data.T3,
            'TT4': data.TT4, 'T4U': data.T4U, 'FTI': data.FTI,
            'on_thyroxine': data.on_thyroxine, 'query_on_thyroxine': data.query_on_thyroxine,
            'on_antithyroid_meds': data.on_antithyroid_meds, 'sick': data.sick,
            'pregnant': data.pregnant, 'thyroid_surgery': data.thyroid_surgery,
            'I131_treatment': data.I131_treatment, 'query_hypothyroid': data.query_hypothyroid,
            'query_hyperthyroid': data.query_hyperthyroid, 'lithium': data.lithium,
            'goitre': data.goitre, 'tumor': data.tumor, 'hypopituitary': data.hypopituitary,
            'psych': data.psych, 'TSH_measured': data.TSH_measured,
            'T3_measured': data.T3_measured, 'TT4_measured': data.TT4_measured,
            'T4U_measured': data.T4U_measured, 'FTI_measured': data.FTI_measured,
            'TBG_measured': data.TBG_measured
        }
    )
    return {
        "disease": "Thyroid Disease",
        "probability": round(prob * 100, 2),
        "risk_level": "High Risk" if prob > 0.5 else "Low Risk",
        "data_shared": "0 bytes",
        "privacy": "Differential Privacy Enabled"
    }