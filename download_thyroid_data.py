# thyroid_federated.py
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, Input
from tensorflow.keras.optimizers import Adam
from sklearn.utils.class_weight import compute_class_weight

np.random.seed(42)
tf.random.set_seed(42)

print("Loading Thyroid Preprocessed Data...")

X_train = np.load('data/thyroid_X_train.npy')
y_train = np.load('data/thyroid_y_train.npy')
X_test = np.load('data/thyroid_X_test.npy')
y_test = np.load('data/thyroid_y_test.npy')

input_dim = X_train.shape[1]
print(f"Data Loaded. Input Features: {input_dim}, Training Samples: {X_train.shape[0]}")

classes = np.unique(y_train)
class_weights_array = compute_class_weight('balanced', classes=classes, y=y_train)
class_weights = dict(zip(classes, class_weights_array))
print(f"Class Weights: {class_weights}")

def create_model():
    model = Sequential([
        Input(shape=(input_dim,)),
        Dense(128, activation='relu'),
        BatchNormalization(),
        Dropout(0.3),
        Dense(64, activation='relu'),
        BatchNormalization(),
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dropout(0.2),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    return model

indices = np.arange(X_train.shape[0])
np.random.shuffle(indices)
X_train, y_train = X_train[indices], y_train[indices]

split1 = int(0.5 * len(X_train))
split2 = int(0.8 * len(X_train))

hospital_data = [
    (X_train[:split1], y_train[:split1]),
    (X_train[split1:split2], y_train[split1:split2]),
    (X_train[split2:], y_train[split2:])
]

global_model = create_model()
global_weights = global_model.get_weights()

rounds = 8
local_epochs = 15
print(f"\nStarting Federated Learning for {rounds} rounds with {local_epochs} local epochs...")

best_accuracy = 0

for round_num in range(1, rounds + 1):
    print(f"\n--- Round {round_num} ---")
    local_weights_list = []
    total_samples = 0
    
    for i, (X_hosp, y_hosp) in enumerate(hospital_data):
        print(f"  Hospital {chr(65+i)} training on {len(X_hosp)} samples...")
        
        local_model = create_model()
        local_model.set_weights(global_weights)
        
        local_model.fit(
            X_hosp, y_hosp,
            epochs=local_epochs,
            batch_size=32,
            verbose=0,
            class_weight=class_weights
        )
        
        local_weights = local_model.get_weights()
        noisy_weights = []
        clip_norm = 1.0
        noise_scale = 0.005
        
        for w in local_weights:
            w_clipped = np.clip(w, -clip_norm, clip_norm)
            noise = np.random.normal(0, noise_scale, w.shape)
            noisy_weights.append(w_clipped + noise)
            
        local_weights_list.append(noisy_weights)
        total_samples += len(X_hosp)
        
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
    
    loss, acc = global_model.evaluate(X_test, y_test, verbose=0)
    print(f"  Global Model Test Accuracy: {acc*100:.2f}%")
    
    if acc > best_accuracy:
        best_accuracy = acc
        global_model.save('thyroid_dp_model.keras')
        print(f"  New best model saved!")

print(f"\n{'='*50}")
print(f"Federated Learning Complete!")
print(f"Best Test Accuracy: {best_accuracy*100:.2f}%")
print(f"Model saved as 'thyroid_dp_model.keras'")
print(f"{'='*50}")