# thyroid_federated.py
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
import os

# Set seed for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

print("Loading Thyroid Preprocessed Data...")

# 1. Load Data
X_train = np.load('data/thyroid_X_train.npy')
y_train = np.load('data/thyroid_y_train.npy')
X_test = np.load('data/thyroid_X_test.npy')
y_test = np.load('data/thyroid_y_test.npy')

input_dim = X_train.shape[1]
print(f"Data Loaded. Input Features: {input_dim}, Training Samples: {X_train.shape[0]}")

# 2. Define Model Architecture
def create_model():
    model = Sequential([
        Dense(64, input_dim=input_dim, activation='relu'),
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dropout(0.2),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid') # Binary classification
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), 
                  loss='binary_crossentropy', 
                  metrics=['accuracy'])
    return model

# 3. Federated Learning Setup (3 Hospitals)
# Split data into 3 parts: 50%, 30%, 20%
indices = np.arange(X_train.shape[0])
np.random.shuffle(indices)
X_train, y_train = X_train[indices], y_train[indices]

split1 = int(0.5 * len(X_train))
split2 = int(0.8 * len(X_train))

hospital_data = [
    (X_train[:split1], y_train[:split1]),               # Hospital A (50%)
    (X_train[split1:split2], y_train[split1:split2]),   # Hospital B (30%)
    (X_train[split2:], y_train[split2:])                # Hospital C (20%)
]

# Initialize Global Model
global_model = create_model()
global_weights = global_model.get_weights()

# 4. Federated Training Loop (3 Rounds)
rounds = 3
print(f"\nStarting Federated Learning for {rounds} rounds...")

for round_num in range(1, rounds + 1):
    print(f"\n--- Round {round_num} ---")
    local_weights_list = []
    total_samples = 0
    
    for i, (X_hosp, y_hosp) in enumerate(hospital_data):
        print(f"  Hospital {chr(65+i)} training on {len(X_hosp)} samples...")
        
        # Initialize local model with global weights
        local_model = create_model()
        local_model.set_weights(global_weights)
        
        # Local training
        local_model.fit(X_hosp, y_hosp, epochs=3, batch_size=32, verbose=0)
        
        # Differential Privacy: Add Gaussian Noise to weights
        local_weights = local_model.get_weights()
        noisy_weights = []
        for w in local_weights:
            noise = np.random.normal(0, 0.01, w.shape) # DP Noise
            noisy_weights.append(w + noise)
            
        local_weights_list.append(noisy_weights)
        total_samples += len(X_hosp)
        
    # 5. Federated Averaging (FedAvg)
    print("  Aggregating weights (FedAvg)...")
    new_global_weights = []
    for weights_tuple in zip(*local_weights_list):
        weighted_sum = np.zeros_like(weights_tuple[0])
        for i, w in enumerate(weights_tuple):
            weight_factor = len(hospital_data[i][0]) / total_samples
            weighted_sum += w * weight_factor
        new_global_weights.append(weighted_sum)
        
    global_weights = new_global_weights
    global_model.set_weights(global_weights)
    
    # Evaluate Global Model
    loss, acc = global_model.evaluate(X_test, y_test, verbose=0)
    print(f"  Global Model Test Accuracy: {acc*100:.2f}%")

# 6. Save Model
model_path = 'thyroid_dp_model.keras'
global_model.save(model_path)
print(f"\nFederated Learning Complete! Model saved as '{model_path}'")