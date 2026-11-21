import pandas as pd

df = pd.read_csv('data/stroke_data.csv')

print("--- Basic Info ---")
print(f"Shape: {df.shape}")

print("\n--- Missing Values ---")
print(df.isnull().sum())

print("\n--- Text Columns (jinhe numbers mein badalna hai) ---")
text_cols = df.select_dtypes(include=['object']).columns.tolist()
print(text_cols)

print("\n--- Unique Values in Text Columns ---")
for col in text_cols:
    print(f"\n{col}:")
    print(df[col].unique())

print("\n--- Target Balance ---")
print(df['stroke'].value_counts())
print(f"Ratio: {df['stroke'].value_counts()[1] / len(df) * 100:.2f}% stroke cases")