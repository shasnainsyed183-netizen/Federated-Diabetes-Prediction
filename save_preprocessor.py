import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1. Data load karein
df = pd.read_csv('data/cleaned_data.csv')

X = df.drop('readmitted', axis=1)
y = df['readmitted']

# 2. Same split karein jaisa baseline mein kiya tha
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Scaler fit karein
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# 4. Scaler aur feature names save karein
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

with open('feature_names.pkl', 'wb') as f:
    pickle.dump(X.columns.tolist(), f)

print("✅ Scaler 'scaler.pkl' mein save ho gaya!")
print(f"✅ {len(X.columns)} Feature names 'feature_names.pkl' mein save ho gaye!")
print(f"\nTotal features: {X.shape[1]}")