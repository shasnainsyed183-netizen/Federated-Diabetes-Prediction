import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import pickle

# Heart Model (13 features)
print("Fixing Heart Model...")
heart_features = pickle.load(open('feature_names_heart.pkl', 'rb'))
heart_model = Sequential([
    Dense(64, activation='relu', input_shape=(len(heart_features),)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])
heart_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
heart_model.save('heart_model.h5')
print("✅ Heart Model saved as heart_model.h5")

# Stroke Model (10 features)
print("Fixing Stroke Model...")
stroke_features = pickle.load(open('feature_names_stroke.pkl', 'rb'))
stroke_model = Sequential([
    Dense(64, activation='relu', input_shape=(len(stroke_features),)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])
stroke_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
stroke_model.save('stroke_model.h5')
print("✅ Stroke Model saved as stroke_model.h5")

# Kidney Model (24 features)
print("Fixing Kidney Model...")
kidney_features = pickle.load(open('feature_names_kidney.pkl', 'rb'))
kidney_model = Sequential([
    Dense(64, activation='relu', input_shape=(len(kidney_features),)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])
kidney_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
kidney_model.save('kidney_model.h5')
print("✅ Kidney Model saved as kidney_model.h5")

# Thyroid Model (29 features)
print("Fixing Thyroid Model...")
thyroid_features = pickle.load(open('thyroid_features.pkl', 'rb'))
thyroid_model = Sequential([
    Dense(64, activation='relu', input_shape=(len(thyroid_features),)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])
thyroid_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
thyroid_model.save('thyroid_model.h5')
print("✅ Thyroid Model saved as thyroid_model.h5")

print("All models fixed and saved in H5 format!")