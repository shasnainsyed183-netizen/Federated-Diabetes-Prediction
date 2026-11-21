import flwr as fl
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import warnings
warnings.filterwarnings("ignore")

# 1. Load data to get input shape
df = pd.read_csv('data/optimized_data.csv')
input_shape = (df.drop('readmitted', axis=1).shape[1],)

# 2. Build an empty model (to save weights)
def get_model():
    model = Sequential([
        Dense(128, activation='relu', input_shape=input_shape),
        Dropout(0.3),
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# 3. Custom Strategy to save the model
class SaveModelStrategy(fl.server.strategy.FedAvg):
    def aggregate_fit(self, server_round, results, failures):
        aggregated_parameters, aggregated_metrics = super().aggregate_fit(server_round, results, failures)
        
        if aggregated_parameters is not None:
            print(f"\n[Server] Saving Global Model for Round {server_round}...")
            ndarrays = fl.common.parameters_to_ndarrays(aggregated_parameters)
            global_model = get_model()
            global_model.set_weights(ndarrays)
            global_model.save("federated_model.h5")
            print(f"[Server] Round {server_round} Model saved as 'federated_model.h5'!\n")
            
        return aggregated_parameters, aggregated_metrics

# 4. Configure Strategy
strategy = SaveModelStrategy(
    fraction_fit=1.0,
    fraction_evaluate=1.0,
    min_fit_clients=3,
    min_evaluate_clients=3,
    min_available_clients=3,
)

# 5. Start Server
if __name__ == "__main__":
    print("[Server] Central Server Starting (Port: 8080)...")
    print("[Server] Waiting for Hospitals (Clients)...")
    
    fl.server.start_server(
        server_address="127.0.0.1:8080",
        config=fl.server.ServerConfig(num_rounds=5),
        strategy=strategy,
    )