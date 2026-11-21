import pandas as pd
import numpy as np

# 1. Load data
df = pd.read_csv('data/cleaned_data.csv')

# 2. Basic info
print("[Features] Shape:", df.shape)
print("-" * 50)
print("[Features] Column Names and Data Types:")
print("-" * 50)

for col in df.columns:
    dtype = df[col].dtype
    unique = df[col].nunique()
    print(f"  {col:30s} | {str(dtype):10s} | Unique: {unique}")

# 3. Check for constant or near-constant columns
print("\n" + "-" * 50)
print("[Features] Low-Variance Columns (Unique <= 2):")
print("-" * 50)
for col in df.columns:
    if df[col].nunique() <= 2:
        print(f"  {col}: {df[col].nunique()} unique values")

# 4. Check correlation with target
print("\n" + "-" * 50)
print("[Features] Correlation with Target (readmitted):")
print("-" * 50)
corr = df.corr()['readmitted'].sort_values(ascending=False)
for col, val in corr.items():
    if col != 'readmitted':
        print(f"  {col:30s} : {val:+.4f}")

# 5. Check for missing values
print("\n" + "-" * 50)
print("[Features] Missing Values:")
print("-" * 50)
missing = df.isnull().sum()
if missing.sum() == 0:
    print("  No missing values.")
else:
    print(missing[missing > 0])