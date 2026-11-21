import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")

print("1. Loading data and preparing a test sample...")
# Load the dataset
df = pd.read_csv('data/cleaned_data.csv')
X = df.drop('readmitted', axis=1)
y = df['readmitted']

# Standardize the data (as we did during training)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Pick the first patient from the dataset for testing
sample_patient = np.array([X_scaled[0]])
actual_result = y.iloc[0]

print("2. Loading the Federated Model (federated_model.h5)...")
# Load the model we just trained and saved
model = load_model('federated_model.h5')

print("3. Making prediction...")
# Get the prediction score (0.0 to 1.0)
prediction_score = model.predict(sample_patient)[0][0]

print("\n" + "="*40)
print(f"Actual Result in Data: {actual_result}")
print(f"Model Prediction Score: {prediction_score:.4f}")

if prediction_score > 0.5:
    print("Model says: Patient WILL be readmitted (1)")
else:
    print("Model says: Patient WILL NOT be readmitted (0)")
print("="*40 + "\n")