import pandas as pd
from sklearn.datasets import fetch_openml

print("Heart Disease dataset download ho raha hai... (1-2 minute lagenge)")

# UCI Heart Disease dataset download karein
heart = fetch_openml(name='heart-disease', version=1, as_frame=True, parser='auto')
df = heart.frame

print(f"\n--- Dataset Successfully Download Ho Gaya ---")
print(f"Shape: {df.shape}")
print(f"\n--- Pehli 5 rows ---")
print(df.head())
print(f"\n--- Columns ---")
print(df.columns.tolist())

# Dataset save karein
df.to_csv('data/heart_disease.csv', index=False)
print("\n✅ Data 'data/heart_disease.csv' mein save ho gaya!")