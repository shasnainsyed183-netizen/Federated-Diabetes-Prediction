"""
Save scalers and feature names for all 3 disease models
This allows the dashboard to make REAL predictions
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# ========================================
# 1. HEART DISEASE PREPROCESSOR
# ========================================
print("=" * 60)
print("Processing Heart Disease...")
print("=" * 60)

df_heart = pd.read_csv('data/heart_disease.csv')

X_heart = df_heart.drop('target', axis=1)
y_heart = df_heart['target']

# Same split as training
X_temp_h, X_test_h, y_temp_h, y_test_h = train_test_split(
    X_heart, y_heart, test_size=0.2, random_state=42
)

scaler_heart = StandardScaler()
scaler_heart.fit(X_temp_h)

with open('scaler_heart.pkl', 'wb') as f:
    pickle.dump(scaler_heart, f)

with open('feature_names_heart.pkl', 'wb') as f:
    pickle.dump(X_heart.columns.tolist(), f)

print(f"✅ Heart scaler saved ({len(X_heart.columns)} features)")
print(f"   Features: {X_heart.columns.tolist()}")


# ========================================
# 2. STROKE PREPROCESSOR
# ========================================
print("\n" + "=" * 60)
print("Processing Stroke...")
print("=" * 60)

df_stroke = pd.read_csv('data/stroke_data.csv')

# Same cleaning as training
df_stroke = df_stroke.drop('id', axis=1)
df_stroke['bmi'] = df_stroke['bmi'].fillna(df_stroke['bmi'].median())
df_stroke = df_stroke[df_stroke['gender'] != 'Other']

df_stroke['gender'] = df_stroke['gender'].map({'Male': 1, 'Female': 0})
df_stroke['ever_married'] = df_stroke['ever_married'].map({'Yes': 1, 'No': 0})
df_stroke['Residence_type'] = df_stroke['Residence_type'].map({'Urban': 1, 'Rural': 0})
df_stroke['smoking_status'] = df_stroke['smoking_status'].map({
    'never smoked': 0, 'formerly smoked': 1, 'smokes': 2, 'Unknown': 3
})
df_stroke = pd.get_dummies(df_stroke, columns=['work_type'], drop_first=True)
df_stroke = df_stroke.astype(float)

X_stroke = df_stroke.drop('stroke', axis=1)
y_stroke = df_stroke['stroke']

X_temp_s, X_test_s, y_temp_s, y_test_s = train_test_split(
    X_stroke, y_stroke, test_size=0.2, random_state=42, stratify=y_stroke
)

scaler_stroke = StandardScaler()
scaler_stroke.fit(X_temp_s)

with open('scaler_stroke.pkl', 'wb') as f:
    pickle.dump(scaler_stroke, f)

with open('feature_names_stroke.pkl', 'wb') as f:
    pickle.dump(X_stroke.columns.tolist(), f)

print(f"✅ Stroke scaler saved ({len(X_stroke.columns)} features)")
print(f"   Features: {X_stroke.columns.tolist()}")


# ========================================
# 3. DIABETES (Already exists, but verify)
# ========================================
print("\n" + "=" * 60)
print("Verifying Diabetes preprocessor...")
print("=" * 60)

import os
if os.path.exists('scaler.pkl') and os.path.exists('feature_names.pkl'):
    with open('feature_names.pkl', 'rb') as f:
        features_d = pickle.load(f)
    print(f"✅ Diabetes preprocessor already exists ({len(features_d)} features)")
else:
    print("⚠️  Diabetes preprocessor missing! Run 'python save_preprocessor.py'")

print("\n" + "=" * 60)
print("🎉 ALL PREPROCESSORS SAVED SUCCESSFULLY!")
print("=" * 60)