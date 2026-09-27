import pandas as pd
import numpy as np
import pickle
import shap
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import tensorflow as tf

print("SHAP Analysis shuru ho raha hai...\n")

# ========================================
# 1. DATA LOAD
# ========================================
df = pd.read_csv('data/cleaned_data.csv')

X = df.drop('readmitted', axis=1)
y = df['readmitted']

# ========================================
# 2. MODEL AUR SCALER LOAD
# ========================================
model = tf.keras.models.load_model('federated_dp_model.keras')

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('feature_names.pkl', 'rb') as f:
    feature_names = pickle.load(f)

print(f"Model loaded: {model.count_params()} parameters")
print(f"Features: {len(feature_names)}")

# ========================================
# 3. SAMPLE DATA (SHAP ke liye 200 samples kaafi hain)
# ========================================
np.random.seed(42)
sample_indices = np.random.choice(len(X), size=200, replace=False)
X_sample = X.iloc[sample_indices]
X_sample_scaled = scaler.transform(X_sample)

print(f"SHAP sample: {X_sample_scaled.shape}\n")

# ========================================
# 4. SHAP EXPLAINER
# ========================================
print("KernelExplainer bana rahe hain... (yeh thoda time lega - 3-5 minute)")

# Background data (SHAP ko reference chahiye)
background = X_sample_scaled[:50]

# Model ka prediction function
def model_predict(data):
    return model.predict(data, verbose=0).flatten()

explainer = shap.KernelExplainer(model_predict, background)

print("SHAP values calculate kar rahe hain... (2-3 minute aur)")
shap_values = explainer.shap_values(X_sample_scaled[:100], nsamples=100)

# ========================================
# 5. FEATURE IMPORTANCE (Top 15)
# ========================================
mean_shap = np.abs(shap_values).mean(axis=0)
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'SHAP Importance': mean_shap
}).sort_values('SHAP Importance', ascending=False)

print("\n========== TOP 15 FEATURES (AI Ke Liye Sab Se Important) ==========")
print(importance_df.head(15).to_string(index=False))

# Save results
importance_df.to_csv('shap_feature_importance.csv', index=False)
print("\n✅ Results saved to 'shap_feature_importance.csv'")

# ========================================
# 6. PLOT BANAYEIN
# ========================================
plt.figure(figsize=(10, 8))
top_15 = importance_df.head(15)
plt.barh(top_15['Feature'][::-1], top_15['SHAP Importance'][::-1], color='steelblue')
plt.xlabel('SHAP Importance (Higher = More Important)')
plt.title('Top 15 Features for Diabetes Readmission Prediction')
plt.tight_layout()
plt.savefig('shap_summary.png', dpi=150, bbox_inches='tight')
plt.close()

print("✅ Plot saved to 'shap_summary.png'")
print("\n========== SHAP Analysis Complete ==========")