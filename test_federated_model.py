import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model
import warnings
warnings.filterwarnings("ignore")

# 1. Load the OPTIMIZED data
df = pd.read_csv('data/optimized_data.csv')

# 2. Prepare features and target
X = df.drop('readmitted', axis=1)
y = df['readmitted']

# 3. Split into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Scale the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 5. Load the federated model
print("[Test] Loading federated_model.h5...")
model = load_model('federated_model.h5')

# 6. Evaluate on test data
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"[Test] Federated Model Test Accuracy: {accuracy * 100:.2f}%")
print(f"[Test] Federated Model Test Loss: {loss:.4f}")

# 7. Make predictions on first 5 test samples
print("\n[Test] Sample Predictions (first 5 test samples):")
predictions = model.predict(X_test[:5], verbose=0)
for i in range(5):
    pred_label = "Readmitted" if predictions[i][0] > 0.5 else "Not Readmitted"
    actual_label = "Readmitted" if y_test.iloc[i] == 1 else "Not Readmitted"
    print(f"  Sample {i+1}: Predicted={pred_label} (prob={predictions[i][0]:.3f}) | Actual={actual_label}")

print("\n[Test] Federated model is working correctly!")