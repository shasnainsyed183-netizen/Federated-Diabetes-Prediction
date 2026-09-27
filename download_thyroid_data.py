"""
Download Thyroid Disease Dataset
Source: UCI Machine Learning Repository
"""

import pandas as pd

print("Thyroid Disease dataset download ho raha hai...")

# UCI Thyroid dataset (working URL)
url = "https://raw.githubusercontent.com/MaskiVal/DataSets/main/thyroid.csv"

try:
    df = pd.read_csv(url)
    print("✅ Thyroid dataset download ho gaya!")
    
    print(f"\n--- Shape ---")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    
    print(f"\n--- Columns ---")
    print(df.columns.tolist())
    
    print(f"\n--- Pehli 5 rows ---")
    print(df.head())
    
    # Save
    df.to_csv('data/thyroid_data.csv', index=False)
    print("\n✅ Data 'data/thyroid_data.csv' mein save ho gaya!")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nAlternate URL try kar rahe hain...")
    
    url2 = "https://raw.githubusercontent.com/plotly/datasets/master/thyroid.csv"
    try:
        df = pd.read_csv(url2)
        df.to_csv('data/thyroid_data.csv', index=False)
        print(f"✅ Alternate URL se download hua! Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
    except Exception as e2:
        print(f"Alternate bhi fail: {e2}")