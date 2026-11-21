import flwr as fl
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import tensorflow_privacy as tfp
import sys
import warnings
warnings.filterwarnings("ignore")

# 1. Load Data
df = pd.read_csv('data/optimized_data.csv')

# 2. Split Data into 3 Hospitals
partition_id = int(sys.argv[1]) if len(sys.argv) > 1 else 0
num_partitions = 3
split_size = len(df) // num_partitions
start_idx = partition_id * split_size
end_idx = (partition_id + 1) * split_size if partition_id < num_partitions - 1 else len(df)

local_df = df.iloc[start_idx:end_idx]
X = local_df.drop('readmitted', axis=1)
y = local_df['readmitted']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# --- DIFFERENTIAL PRIVACY FIX (Batch Size & Drop Remainder) ---
batch_size = 32

# tf.data.Dataset use kiya hai taake aakhri adhoora batch drop ho jaye aur error na aaye
train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))
train_dataset = train_dataset.shuffle(buffer_size=1024).batch(batch_size, drop_remainder=True)

test_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test))
test_dataset = test_dataset.batch(batch_size)

# 3. Build Model
model = Sequential([
    Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])

# DP-SGD Setup
loss_fn = tf.keras.losses.BinaryCrossentropy(
    from_logits=False, 
    reduction=tf.keras.losses.Reduction.NONE
)

dp_optimizer = tfp.DPKerasSGDOptimizer(
    l2_norm_clip=1.0,
    noise_multiplier=1.1,
    num_microbatches=batch_size,
    learning_rate=0.01
)
model.compile(optimizer=dp_optimizer, loss=loss_fn, metrics=['accuracy'])

# 4. Flower Client Class
class HospitalClient(fl.client.NumPyClient):
    def get_parameters(self, config):
        return model.get_weights()

    def fit(self, parameters, config):
        model.set_weights(parameters)
        # Dataset pass kiya hai
        model.fit(train_dataset, epochs=3, verbose=0)
        return model.get_weights(), len(X_train), {}

    def evaluate(self, parameters, config):
        model.set_weights(parameters)
        # Dataset pass kiya hai
        loss, accuracy = model.evaluate(test_dataset, verbose=0)
        print(f"[Hospital {partition_id} - DP] Local Accuracy: {accuracy*100:.2f}%")
        return loss, len(X_test), {"accuracy": float(accuracy)}

# 5. Start Client
print(f"[Hospital {partition_id} - DP] Starting... (Waiting for Server)")
fl.client.start_client(
    server_address="127.0.0.1:8080",
    client=HospitalClient().to_client(),
)