import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
import copy

# ========================================
# 1. DATA LOAD AUR SPLIT
# ========================================
df = pd.read_csv('data/cleaned_data.csv')

X = df.drop('readmitted', axis=1)
y = df['readmitted']

X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3 hospitals mein data baantein
X_a, X_temp2, y_a, y_temp2 = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
X_b, X_c, y_b, y_c = train_test_split(X_temp2, y_temp2, test_size=0.4, random_state=42)

scaler = StandardScaler()
X_a = scaler.fit_transform(X_a)
X_b = scaler.transform(X_b)
X_c = scaler.transform(X_c)
X_test = scaler.transform(X_test)

print(f"Hospital A: {len(X_a)} patients")
print(f"Hospital B: {len(X_b)} patients")
print(f"Hospital C: {len(X_c)} patients")

# ========================================
# 2. MODEL FUNCTION
# ========================================
def create_model(input_dim):
    model = Sequential([
        Input(shape=(input_dim,)),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# ========================================
# 3. DIFFERENTIAL PRIVACY: WEIGHTS MEIN NOISE ADD KAREIN
# ========================================
def add_dp_noise(weights, noise_multiplier, clip_norm=1.0):
    """
    Har weight ko clip karein aur usme Gaussian noise add karein.
    noise_multiplier zyada = zyada privacy, lekin kam accuracy.
    """
    noisy_weights = []
    for layer in weights:
        # 1. Weight clipping (sensitivity limit)
        clipped = np.clip(layer, -clip_norm, clip_norm)
        # 2. Gaussian noise add karein
        noise = np.random.normal(0, noise_multiplier * clip_norm, clipped.shape)
        noisy_weights.append(clipped + noise)
    return noisy_weights

# ========================================
# 4. FEDERATED AVERAGING (FedAvg)
# ========================================
def federated_averaging(client_weights):
    avg_weights = []
    num_clients = len(client_weights)
    for layer_idx in range(len(client_weights[0])):
        layer_avg = np.zeros_like(client_weights[0][layer_idx])
        for client in client_weights:
            layer_avg += client[layer_idx]
        layer_avg = layer_avg / num_clients
        avg_weights.append(layer_avg)
    return avg_weights

# ========================================
# 5. FEDERATED TRAINING WITH DP
# ========================================
NUM_ROUNDS = 5
LOCAL_EPOCHS = 3
NOISE_MULTIPLIER = 0.01   # Noise level (zyada = zyada privacy)

# Global model
global_model = create_model(X_a.shape[1])

hospitals = [
    ("Hospital A", X_a, y_a),
    ("Hospital B", X_b, y_b),
    ("Hospital C", X_c, y_c)
]

print("\n========== FEDERATED LEARNING WITH DIFFERENTIAL PRIVACY ==========")
print(f"Noise Multiplier: {NOISE_MULTIPLIER}")
print("=" * 65)

for round_num in range(1, NUM_ROUNDS + 1):
    print(f"\n----- Round {round_num}/{NUM_ROUNDS} -----")
    
    global_weights = global_model.get_weights()
    client_weights = []
    
    for name, X_hosp, y_hosp in hospitals:
        local_model = create_model(X_hosp.shape[1])
        local_model.set_weights(copy.deepcopy(global_weights))
        local_model.fit(X_hosp, y_hosp, epochs=LOCAL_EPOCHS, batch_size=32, verbose=0)
        
        # DP: Local weights mein noise add karein
        local_weights = local_model.get_weights()
        noisy_weights = add_dp_noise(local_weights, NOISE_MULTIPLIER)
        client_weights.append(noisy_weights)
        
        print(f"  {name}: Training + DP Noise add hua ({len(X_hosp)} patients)")
    
    # FedAvg
    new_global_weights = federated_averaging(client_weights)
    global_model.set_weights(new_global_weights)
    
    loss, acc = global_model.evaluate(X_test, y_test, verbose=0)
    print(f"  Global Model Accuracy: {acc * 100:.2f}%")

# ========================================
# 6. FINAL RESULTS
# ========================================
print("\n" + "=" * 65)
print("========== FINAL COMPARISON ==========")
loss, dp_accuracy = global_model.evaluate(X_test, y_test, verbose=0)
print(f"Baseline (Centralized) Accuracy:       62.34%")
print(f"Federated Learning (No DP) Accuracy:   61.95%")
print(f"Federated Learning with DP Accuracy:   {dp_accuracy * 100:.2f}%")
print("=" * 65)

# DP model save karein
global_model.save('federated_dp_model.keras')
print("\n✅ DP Model 'federated_dp_model.keras' mein save ho gaya!")