import pandas as pd

print("Stroke dataset download ho raha hai...")

# Naya reliable URL (GitHub raw link)
url = "https://raw.githubusercontent.com/Center-for-Health-Data-Science/PythonTsunami/refs/heads/2024_Oct/Exercise/datasets/healthcare-dataset-stroke-data.csv"

try:
    # Seedha pandas se load karein
    df = pd.read_csv(url)
    print("✅ Stroke dataset download ho gaya!")
    
    print(f"\n--- Shape ---")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    
    print(f"\n--- Pehli 5 rows ---")
    print(df.head())
    
    print(f"\n--- Columns ---")
    print(df.columns.tolist())
    
    print(f"\n--- Target Distribution ---")
    print(df['stroke'].value_counts())
    
    # Save karein
    df.to_csv('data/stroke_data.csv', index=False)
    print("\n✅ Data 'data/stroke_data.csv' mein save ho gaya!")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nAlternate URL try kar rahe hain...")
    url2 = "https://raw.githubusercontent.com/SunnyRao07/stroke-risk-prediction/main/healthcare-dataset-stroke-data.csv"
    try:
        df = pd.read_csv(url2)
        df.to_csv('data/stroke_data.csv', index=False)
        print("✅ Alternate URL se download ho gaya!")
        print(f"Shape: {df.shape}")
    except Exception as e2:
        print(f"Alternate URL bhi fail: {e2}")