"""
Download Kidney Disease Dataset
Source: UCI Machine Learning Repository (via GitHub)
"""

import pandas as pd

print("Kidney Disease dataset download ho raha hai...")

# Working direct URL
url = "https://raw.githubusercontent.com/MaskiVal/DataSets/main/kidney_disease.csv"

try:
    df = pd.read_csv(url)
    print("✅ Kidney dataset download ho gaya!")
    
    print(f"\n--- Shape ---")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    
    print(f"\n--- Columns ---")
    print(df.columns.tolist())
    
    print(f"\n--- Pehli 5 rows ---")
    print(df.head())
    
    print(f"\n--- Target (classification) Distribution ---")
    print(df['classification'].value_counts())
    
    # Save karein
    df.to_csv('data/kidney_data.csv', index=False)
    print("\n✅ Data 'data/kidney_data.csv' mein save ho gaya!")
    
except Exception as e:
    print(f"Error: {e}")