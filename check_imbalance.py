import pandas as pd

# 1. Load data
df = pd.read_csv('data/cleaned_data.csv')

# 2. Check target distribution
print("[Check] Target Column: readmitted")
print("-" * 40)
counts = df['readmitted'].value_counts()
print(counts)
print("-" * 40)

# 3. Calculate percentages
total = len(df)
for label, count in counts.items():
    print(f"  Class {label}: {count} ({count/total*100:.2f}%)")

# 4. Check imbalance ratio
majority = counts.max()
minority = counts.min()
ratio = majority / minority
print("-" * 40)
print(f"[Check] Imbalance Ratio: {ratio:.2f} : 1")

if ratio > 3:
    print("[Check] WARNING: Data is highly imbalanced. We need to fix this!")
else:
    print("[Check] Data is reasonably balanced.")