import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_class_weight
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
import copy

# ========================================
# 1. DATA LOAD
# ========================================
df = pd.read_csv('data/stroke_data.csv')

# 2. 'id' column hata dein (sirf roll number hai)
df = df.drop('id', axis=1)

# 3. BMI missing values ko median se fill karein
df['bmi'] = df['bmi'].fillna(df['bmi'].median())

# 4. 'Other' gender wali row hata dein (sirf 1 hai)
df = df[df['gender'] != 'Other']

# 5. Text columns ko numbers mein badlein
df['gender'] = df['gender'].map({'Male': 1, 'Female': 0})
df['ever_married'] = df['ever_married'].map({'Yes': 1, 'No': 0})
df['Residence_type'] = df['Residence_type'].map({'Urban': 1, 'Rural': 0})
df['smoking_status'] = df['smoking_status'].map({
    'never smoked': 0, 'formerly smoked': 1, 'smokes': 2, 'Unknown': 3
})

# Work type ko one-hot encoding karein
df = pd.get_dummies(df, columns=['work_type'], drop_first=True)

# 6. Sab kuch float mein convert karein
df = df.astype(float)

print(f"--- Cleaned Data Shape ---")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
print(f"Stroke cases: {df['stroke'].sum():.0f} ({df['stroke'].mean()*100:.2f}%)")

# ========================================
# 7. TRAIN / TEST SPLIT
# ========================================
X = df.drop('stroke', axis=1)
y = df['stroke']

X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 3 hospitals mein baantein
X_a, X_temp2, y_a, y_temp2 = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)
X_b, X_c, y_b, y_c = train_test_split(X_temp2, y_temp2, test_size=0.4, random_state=42, stratify=y_temp2)

print(f"\nHospital A: {len(X_a)} patients ({y_a.sum():.0f} strokes)")
print(f"Hospital B: {len(X_b)} patients ({y_b.sum():.0f} strokes)")
print(f"Hospital C: {len(X_c)} patients ({y_c.sum():.0f} strokes)")
print(f"Test Data:  {len(X_test)} patients ({y_test.sum():.0f} strokes)")

# Standardize
scaler = StandardScaler()
X_a = scaler.fit_transform(X_a)
X_b = scaler.transform(X_b)
X_c = scaler.transform(X_c)
X_test = scaler.transform(X_test)

# ========================================
# 8. CLASS WEIGHTS (Imbalance Handle Karne Ke Liye)
# ========================================
classes = np.unique(y_temp)
weights = compute_class_weight('balanced', classes=classes, y=y_temp)
class_weight_dict = dict(zip(classes, weights))
print(f"\n--- Class Weights (imbalance handle) ---")
print(f"No Stroke: {class_weight_dict[0.0]:.2f}")
print(f"Stroke:    {class_weight_dict[1.0]:.2f}")

# ========================================
# 9. MODEL FUNCTION
# ========================================
def create_model(input_dim):
    model = Sequential([
        Input(shape=(input_dim,)),
        Dense(32, activation='relu'),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# ========================================
# 10. DIFFERENTIAL PRIVACY NOISE
# ========================================
def add_dp_noise(weights, noise_multiplier, clip_norm=1.0):
    noisy_weights = []
    for layer in weights:
        clipped = np.clip(layer, -clip_norm, clip_norm)
        noise = np.random.normal(0, noise_multiplier * clip_norm, clipped.shape)
        noisy_weights.append(clipped + noise)
    return noisy_weights

# ========================================
# 11. FEDERATED AVERAGING
# ========================================
def federated_averaging(client_weights):
    avg_weights = []
    for layer_idx in range(len(client_weights[0])):
        layer_avg = np.zeros_like(client_weights[0][layer_idx])
        for client in client_weights:
            layer_avg += client[layer_idx]
        layer_avg = layer_avg / len(client_weights)
        avg_weights.append(layer_avg)
    return avg_weights

# ========================================
# 12. FEDERATED LEARNING + DP
# ========================================
NUM_ROUNDS = 10
LOCAL_EPOCHS = 5
NOISE_MULTIPLIER = 0.01

global_model = create_model(X_a.shape[1])

hospitals = [
    ("Hospital A", X_a, y_a),
    ("Hospital B", X_b, y_b),
    ("Hospital C", X_c, y_c)
]

print("\n========== STROKE: FEDERATED LEARNING + DP ==========\n")

for round_num in range(1, NUM_ROUNDS + 1):
    global_weights = global_model.get_weights()
    client_weights = []
    
    for name, X_hosp, y_hosp in hospitals:
        local_model = create_model(X_hosp.shape[1])
        local_model.set_weights(copy.deepcopy(global_weights))
        local_model.fit(X_hosp, y_hosp, epochs=LOCAL_EPOCHS, batch_size=32, verbose=0,
                       class_weight=class_weight_dict)
        
        local_weights = local_model.get_weights()
        noisy_weights = add_dp_noise(local_weights, NOISE_MULTIPLIER)
        client_weights.append(noisy_weights)
    
    new_global_weights = federated_averaging(client_weights)
    global_model.set_weights(new_global_weights)
    
    loss, acc = global_model.evaluate(X_test, y_test, verbose=0)
    print(f"Round {round_num}/{NUM_ROUNDS} - Accuracy: {acc * 100:.2f}%")

# ========================================
# 13. FINAL RESULT
# ========================================
print("\n" + "=" * 60)
loss, accuracy = global_model.evaluate(X_test, y_test, verbose=0)
print(f"STROKE MODEL FINAL ACCURACY: {accuracy * 100:.2f}%")
print("=" * 60)

# Extra metrics
from sklearn.metrics import classification_report, confusion_matrix
y_pred = (global_model.predict(X_test, verbose=0) > 0.5).astype(int)
print("\n--- Classification Report ---")
print(classification_report(y_test, y_pred, target_names=['No Stroke', 'Stroke']))
print("--- Confusion Matrix ---")
print(confusion_matrix(y_test, y_pred))

# Save
global_model.save('stroke_dp_model.keras')
print("\n✅ Model 'stroke_dp_model.keras' mein save ho gaya!")