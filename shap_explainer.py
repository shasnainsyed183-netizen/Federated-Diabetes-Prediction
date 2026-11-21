"""
MediFederate SHAP Explainability
Analyze feature importance for all 4 disease models
"""

import pandas as pd
import numpy as np
import pickle
import shap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tensorflow as tf
import os
from sklearn.preprocessing import LabelEncoder


# ========================================
# PREPROCESSING FUNCTIONS
# ========================================

def preprocess_stroke(df):
    """Same preprocessing as stroke_federated.py"""
    df = df.drop('id', axis=1)
    df['bmi'] = df['bmi'].fillna(df['bmi'].median())
    df = df[df['gender'] != 'Other']
    df['gender'] = df['gender'].map({'Male': 1, 'Female': 0})
    df['ever_married'] = df['ever_married'].map({'Yes': 1, 'No': 0})
    df['Residence_type'] = df['Residence_type'].map({'Urban': 1, 'Rural': 0})
    df['smoking_status'] = df['smoking_status'].map({
        'never smoked': 0, 'formerly smoked': 1, 'smokes': 2, 'Unknown': 3
    })
    df = pd.get_dummies(df, columns=['work_type'], drop_first=True)
    df = df.astype(float)
    return df


def preprocess_kidney(df):
    """Same preprocessing as kidney_federated.py"""
    df = df.drop('id', axis=1)
    df['classification'] = df['classification'].astype(str).str.strip()
    df['classification'] = df['classification'].replace({'ckd\t': 'ckd'})
    df['classification'] = df['classification'].map({'ckd': 1, 'notckd': 0})
    df = df.dropna(subset=['classification'])
    df['classification'] = df['classification'].astype(int)
    
    # Encode categorical columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
    
    df = df.apply(pd.to_numeric, errors='coerce')
    for col in df.columns:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())
    df = df.astype(float)
    return df


# ========================================
# SHAP FUNCTION
# ========================================

def explain_model(model_name, model_file, scaler_file, data_file, target_col,
                  feature_file, preprocess_func=None, max_samples=100):
    """Generate SHAP analysis for a given disease model"""
    
    print(f"\n{'='*60}")
    print(f"SHAP Analysis: {model_name}")
    print(f"{'='*60}\n")
    
    if not os.path.exists(model_file):
        print(f"❌ Model not found: {model_file}")
        return False
    
    # Load data
    df = pd.read_csv(data_file)
    
    # Apply preprocessing if provided
    if preprocess_func:
        df = preprocess_func(df)
        print(f"Preprocessed data shape: {df.shape}")
    
    # Load model
    model = tf.keras.models.load_model(model_file)
    
    with open(scaler_file, 'rb') as f:
        scaler = pickle.load(f)
    
    with open(feature_file, 'rb') as f:
        feature_names = pickle.load(f)
    
    # Prepare data
    X = df.drop(target_col, axis=1)
    
    # Ensure column order matches feature_names
    X = X[feature_names]
    
    # Sample data
    np.random.seed(42)
    if len(X) > max_samples:
        sample_indices = np.random.choice(len(X), size=max_samples, replace=False)
        X_sample = X.iloc[sample_indices]
    else:
        X_sample = X
    
    X_scaled = scaler.transform(X_sample)
    
    print(f"Model loaded: {model.count_params()} parameters")
    print(f"Features: {len(feature_names)}")
    print(f"Sample size: {len(X_scaled)}\n")
    
    # SHAP Explainer
    print("Creating SHAP explainer...")
    background = X_scaled[:30]
    
    def model_predict(data):
        return model.predict(data, verbose=0).flatten()
    
    explainer = shap.KernelExplainer(model_predict, background)
    
    print("Calculating SHAP values (1-2 minutes)...")
    shap_values = explainer.shap_values(X_scaled[:50], nsamples=100)
    
    # Feature importance
    mean_shap = np.abs(shap_values).mean(axis=0)
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'SHAP Importance': mean_shap
    }).sort_values('SHAP Importance', ascending=False)
    
    print(f"\nTop 10 Features for {model_name}:")
    print(importance_df.head(10).to_string(index=False))
    
    # Save
    safe_name = model_name.lower().replace(' ', '_')
    csv_name = f"shap_{safe_name}_importance.csv"
    importance_df.to_csv(csv_name, index=False)
    print(f"\n✅ Saved: {csv_name}")
    
    # Plot
    plt.figure(figsize=(10, 6))
    top_10 = importance_df.head(10)
    plt.barh(top_10['Feature'][::-1], top_10['SHAP Importance'][::-1], color='steelblue')
    plt.xlabel('SHAP Importance')
    plt.title(f'Top 10 Features - {model_name}')
    plt.tight_layout()
    
    png_name = f"shap_{safe_name}.png"
    plt.savefig(png_name, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Saved: {png_name}")
    return True


# ========================================
# RUN ALL 4 DISEASES
# ========================================
if __name__ == "__main__":
    print("=" * 60)
    print("MediFederate — SHAP Analysis for All 4 Models")
    print("=" * 60)
    
    results = []
    
    # 1. Diabetes (already clean)
    results.append(explain_model(
        "Diabetes",
        "federated_dp_model.keras",
        "scaler.pkl",
        "data/cleaned_data.csv",
        "readmitted",
        "feature_names.pkl",
        preprocess_func=None,
    ))
    
    # 2. Heart Disease (already clean)
    results.append(explain_model(
        "Heart Disease",
        "heart_dp_model.keras",
        "scaler_heart.pkl",
        "data/heart_disease.csv",
        "target",
        "feature_names_heart.pkl",
        preprocess_func=None,
    ))
    
    # 3. Stroke (needs preprocessing)
    results.append(explain_model(
        "Stroke",
        "stroke_dp_model.keras",
        "scaler_stroke.pkl",
        "data/stroke_data.csv",
        "stroke",
        "feature_names_stroke.pkl",
        preprocess_func=preprocess_stroke,
    ))
    
    # 4. Kidney (needs preprocessing)
    results.append(explain_model(
        "Kidney Disease",
        "kidney_dp_model.keras",
        "scaler_kidney.pkl",
        "data/kidney_data.csv",
        "classification",
        "feature_names_kidney.pkl",
        preprocess_func=preprocess_kidney,
    ))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for i, (name, success) in enumerate(zip(
        ["Diabetes", "Heart Disease", "Stroke", "Kidney Disease"],
        results
    )):
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{i+1}. {name}: {status}")
    print("=" * 60)