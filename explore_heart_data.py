import pandas as pd

# Data load karein
df = pd.read_csv('data/heart_disease.csv')

# 1. Basic info
print("--- Basic Information ---")
print(f"Shape: {df.shape}")
print(f"Total missing values: {df.isnull().sum().sum()}")

# 2. Missing values per column
print("\n--- Missing Values Per Column ---")
print(df.isnull().sum())

# 3. Target distribution
print("\n--- Target Distribution ---")
print(df['target'].value_counts())

# 4. Data types
print("\n--- Data Types ---")
print(df.dtypes)