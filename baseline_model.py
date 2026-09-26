import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# 1. Data load karein
df = pd.read_csv('data/cleaned_data.csv')

# 2. Features (X) aur Target (y) alag karein
X = df.drop('readmitted', axis=1)
y = df['readmitted']

# 3. Data ko Train aur Test mein tod dein (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Data ko Standardize karein (Neural Network ke liye zaroori hai)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 5. AI Model banayein (Simple Neural Network)
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')  # 0 ya 1 predict karne ke liye
])

# 6. Model ko compile karein
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 7. Model ko train karein
print("--- Model Train Ho Raha Hai (2-3 minute lagenge) ---")
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1)

# 8. Model ki accuracy check karein
loss, accuracy = model.evaluate(X_test, y_test)
print(f"\n--- Test Accuracy: {accuracy * 100:.2f}% ---")

# 9. Model ko save karein
model.save('baseline_model.h5')
print("\n--- Model 'baseline_model.h5' mein save ho gaya! ---")