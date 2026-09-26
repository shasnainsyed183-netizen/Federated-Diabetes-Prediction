import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
import copy

# ========================================
# 1. DATA LOAD KAREIN
# ========================================
df = pd.read_csv('data/cleaned_data.csv')

X = df.drop('readmitted', axis=1)
y = df['readmitted']

# Pehle train/test split karein (test data sirf final evaluation ke liye)
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Ab train data ko 3 "hospitals" mein baant dein
# Hospital A: 50%, Hospital B: 30%, Hospital C: 20%
X_a, X_temp2, y_a, y_temp2 = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
X_b, X_c, y_b, y_c = train_test_split(X_temp2, y_temp2, test_size=0.4, random_state=42)

print(f"Hospital A: {len(X_a)} patients")
print(f"Hospital B: {len(X_b)} patients")
print(f"Hospital C: {len(X_c)} patients")
print(f"Test Data: {len(X_test)} patients")

# Standardize karein (test data ke saath)
scaler = StandardScaler()
X_a = scaler.fit_transform(X_a)
X_b = scaler.transform(X_b)
X_c = scaler.transform(X_c)
X_test = scaler.transform(X_test)

# ========================================
# 2. MODEL BANANE KA FUNCTION
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
# 3. FEDERATED AVERAGING (FedAvg) ALGORITHM
# ========================================
def federated_averaging(client_weights):
    """Saare hospitals ke weights ka average lein."""
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
# 4. FEDERATED LEARNING TRAINING
# ========================================
NUM_ROUNDS = 5           # Kitne rounds honge
LOCAL_EPOCHS = 3         # Har round mein har hospital kitna train karega

# Global model banayein
global_model = create_model(X_a.shape[1])

hospitals = [
    ("Hospital A", X_a, y_a),
    ("Hospital B", X_b, y_b),
    ("Hospital C", X_c, y_c)
]

print("\n========== FEDERATED LEARNING SHURU ==========\n")

for round_num in range(1, NUM_ROUNDS + 1):
    print(f"\n----- Round {round_num}/{NUM_ROUNDS} -----")
    
    # Global model ke weights sab hospitals ko bhejein
    global_weights = global_model.get_weights()
    client_weights = []
    
    for name, X_hosp, y_hosp in hospitals:
        # Har hospital global weights se shuru kare
        local_model = create_model(X_hosp.shape[1])
        local_model.set_weights(copy.deepcopy(global_weights))
        
        # Local training (data hospital se bahar nahi jata)
        local_model.fit(X_hosp, y_hosp, epochs=LOCAL_EPOCHS, batch_size=32, verbose=0)
        
        # Sirf weights collect karein (data nahi)
        client_weights.append(local_model.get_weights())
        print(f"  {name}: Local training mukammal ({len(X_hosp)} patients)")
    
    # FedAvg: saare weights ka average lein
    new_global_weights = federated_averaging(client_weights)
    global_model.set_weights(new_global_weights)
    
    # Har round ke baad accuracy check karein
    loss, acc = global_model.evaluate(X_test, y_test, verbose=0)
    print(f"  Global Model Accuracy: {acc * 100:.2f}%")

# ========================================
# 5. FINAL RESULTS
# ========================================
print("\n========== FINAL RESULT ==========")
loss, accuracy = global_model.evaluate(X_test, y_test, verbose=0)
print(f"Federated Learning Model Accuracy: {accuracy * 100:.2f}%")
print(f"Baseline Model Accuracy:           62.34%")

# Model save karein
global_model.save('federated_model.keras')
print("\n--- Federated Model 'federated_model.keras' mein save ho gaya! ---")