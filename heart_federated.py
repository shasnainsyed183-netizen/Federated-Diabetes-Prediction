import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
import copy

# ========================================
# 1. DATA LOAD
# ========================================
df = pd.read_csv('data/heart_disease.csv')

X = df.drop('target', axis=1)
y = df['target']

# Train/test split
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3 hospitals mein baantein
X_a, X_temp2, y_a, y_temp2 = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
X_b, X_c, y_b, y_c = train_test_split(X_temp2, y_temp2, test_size=0.4, random_state=42)

print(f"Hospital A: {len(X_a)} patients")
print(f"Hospital B: {len(X_b)} patients")
print(f"Hospital C: {len(X_c)} patients")
print(f"Test Data: {len(X_test)} patients")

# Standardize
scaler = StandardScaler()
X_a = scaler.fit_transform(X_a)
X_b = scaler.transform(X_b)
X_c = scaler.transform(X_c)
X_test = scaler.transform(X_test)

# ========================================
# 2. MODEL FUNCTION
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
# 3. DIFFERENTIAL PRIVACY NOISE
# ========================================
def add_dp_noise(weights, noise_multiplier, clip_norm=1.0):
    noisy_weights = []
    for layer in weights:
        clipped = np.clip(layer, -clip_norm, clip_norm)
        noise = np.random.normal(0, noise_multiplier * clip_norm, clipped.shape)
        noisy_weights.append(clipped + noise)
    return noisy_weights

# ========================================
# 4. FEDERATED AVERAGING
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
# 5. FEDERATED LEARNING + DP
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

print("\n========== HEART DISEASE: FEDERATED LEARNING + DP ==========\n")

for round_num in range(1, NUM_ROUNDS + 1):
    global_weights = global_model.get_weights()
    client_weights = []
    
    for name, X_hosp, y_hosp in hospitals:
        local_model = create_model(X_hosp.shape[1])
        local_model.set_weights(copy.deepcopy(global_weights))
        local_model.fit(X_hosp, y_hosp, epochs=LOCAL_EPOCHS, batch_size=16, verbose=0)
        
        local_weights = local_model.get_weights()
        noisy_weights = add_dp_noise(local_weights, NOISE_MULTIPLIER)
        client_weights.append(noisy_weights)
    
    new_global_weights = federated_averaging(client_weights)
    global_model.set_weights(new_global_weights)
    
    loss, acc = global_model.evaluate(X_test, y_test, verbose=0)
    print(f"Round {round_num}/{NUM_ROUNDS} - Accuracy: {acc * 100:.2f}%")

# ========================================
# 6. FINAL RESULT
# ========================================
print("\n" + "=" * 60)
loss, accuracy = global_model.evaluate(X_test, y_test, verbose=0)
print(f"HEART DISEASE MODEL FINAL ACCURACY: {accuracy * 100:.2f}%")
print("=" * 60)

# Save model
global_model.save('heart_dp_model.keras')
print("\n✅ Model 'heart_dp_model.keras' mein save ho gaya!")