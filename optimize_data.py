import pandas as pd
import numpy as np

# 1. Load data
df = pd.read_csv('data/cleaned_data.csv')
print(f"[Optimize] Original shape: {df.shape}")

# 2. Drop useless columns (only 1 unique value)
useless_cols = []
for col in df.columns:
    if df[col].nunique() <= 1 and col != 'readmitted':
        useless_cols.append(col)
print(f"[Optimize] Dropping useless columns: {useless_cols}")
df = df.drop(columns=useless_cols)

# 3. Drop low-correlation features (threshold = 0.02)
target = 'readmitted'
corr = df.corr()[target].abs()
low_corr_cols = corr[corr < 0.02].index.tolist()
low_corr_cols = [c for c in low_corr_cols if c != target]

print(f"[Optimize] Dropping {len(low_corr_cols)} low-correlation features:")
for c in low_corr_cols:
    print(f"   - {c} (corr={df.corr()[target][c]:+.4f})")

df = df.drop(columns=low_corr_cols)

# 4. Save optimized data
df.to_csv('data/optimized_data.csv', index=False)
print(f"\n[Optimize] Optimized shape: {df.shape}")
print(f"[Optimize] Saved as 'data/optimized_data.csv'")

# 5. Show remaining features
print(f"\n[Optimize] Remaining features ({len(df.columns)-1}):")
for c in df.columns:
    if c != target:
        print(f"   {c}: {df.corr()[target][c]:+.4f}")