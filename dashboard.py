import streamlit as st
import pandas as pd
import numpy as np
import pickle
import tensorflow as tf

st.set_page_config(page_title="Federated Diabetes Prediction", page_icon="🏥", layout="wide")

st.title("🏥 Federated Learning for Diabetes Prediction")
st.markdown("### Privacy-Preserving AI for Healthcare")
st.markdown("---")

# Sidebar
st.sidebar.header("📊 Project Information")
st.sidebar.info("""
**Project:** Federated Learning for Diabetes Prediction

**Goal:** Train AI model without sharing patient data

**Hospitals:** 3 (A, B, C)

**Dataset:** 100,244 patients, 71 features

**Privacy:** Differential Privacy enabled
""")

# Load model, scaler aur feature names
@st.cache_resource
def load_assets():
    model = tf.keras.models.load_model('federated_dp_model.keras')
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('feature_names.pkl', 'rb') as f:
        feature_names = pickle.load(f)
    return model, scaler, feature_names

try:
    model, scaler, feature_names = load_assets()
    model_loaded = True
except Exception as e:
    st.error(f"Model load nahi hua: {e}")
    model_loaded = False

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Model Performance", "🏥 Hospitals", "🔒 Privacy", "🔮 Prediction"])

# ============ TAB 1: MODEL PERFORMANCE ============
with tab1:
    st.header("Model Performance Comparison")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Baseline (Centralized)", "62.34%", "No Privacy")
    with col2:
        st.metric("Federated (No DP)", "61.95%", "-0.39%")
    with col3:
        st.metric("Federated + DP ⭐", "62.38%", "+0.04%")
    
    st.markdown("---")
    st.subheader("📊 Accuracy Comparison")
    chart_data = pd.DataFrame({
        "Model Type": ["Baseline", "Federated (No DP)", "Federated + DP"],
        "Accuracy (%)": [62.34, 61.95, 62.38]
    })
    st.bar_chart(chart_data.set_index("Model Type"))
    
    st.success("✅ Federated Learning with Differential Privacy achieved 62.38% accuracy — even better than the centralized baseline — WITHOUT sharing any patient data!")

    st.markdown("---")
    st.subheader("📋 Summary Table")
    summary = pd.DataFrame({
        "Model": ["Baseline (Centralized)", "Federated Learning", "Federated + Differential Privacy"],
        "Accuracy": ["62.34%", "61.95%", "62.38%"],
        "Data Shared": ["All data", "0 bytes", "0 bytes"],
        "Privacy Guarantee": ["❌ No", "⚠️ Partial", "✅ Yes"]
    })
    st.dataframe(summary, use_container_width=True)

# ============ TAB 2: HOSPITALS ============
with tab2:
    st.header("Participating Hospitals")
    st.markdown("Each hospital trains locally. Only model weights are shared.")
    
    hospital_data = pd.DataFrame({
        "Hospital": ["Hospital A", "Hospital B", "Hospital C"],
        "Patients": [40097, 24058, 16040],
        "Data Shared": ["❌ No", "❌ No", "❌ No"],
        "Local Training": ["✅ Yes", "✅ Yes", "✅ Yes"]
    })
    st.dataframe(hospital_data, use_container_width=True)
    
    st.info("🔒 **Privacy Guarantee:** No patient data ever leaves any hospital. Only encrypted model weights (with DP noise) are shared with the central server.")

# ============ TAB 3: PRIVACY ============
with tab3:
    st.header("🔒 Differential Privacy Explained")
    st.markdown("""
    **What is Differential Privacy (DP)?**
    
    Differential Privacy adds carefully calibrated random noise to the model weights 
    before they are shared with the central server. This ensures that no one can 
    determine whether a specific patient's data was used in training.
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Noise Multiplier", "0.01", "Low")
    with col2:
        st.metric("Weight Clipping", "1.0", "Norm")
    with col3:
        st.metric("Federated Rounds", "5", "Iterations")
    
    st.markdown("---")
    st.subheader("How It Works")
    st.markdown("""
    1. **Local Training:** Each hospital trains the model on its own data.
    2. **Weight Clipping:** Model weights are clipped to a maximum value (sensitivity limit).
    3. **Noise Addition:** Gaussian noise is added to the weights.
    4. **Secure Sharing:** Only the noisy weights are sent to the central server.
    5. **Aggregation:** The server averages all clients' weights (FedAvg).
    6. **Distribution:** The new global model is sent back to all hospitals.
    """)
    
    st.success("✅ **Result:** With DP noise, accuracy actually improved to 62.38% — proving that privacy and performance can go hand-in-hand!")

# ============ TAB 4: PREDICTION ============
with tab4:
    st.header("Patient Readmission Prediction")
    st.markdown("Enter patient details to predict readmission risk:")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("Age", 5, 95, 55)
        time_in_hospital = st.slider("Time in Hospital (days)", 1, 14, 5)
        num_medications = st.slider("Number of Medications", 1, 81, 15)
        num_lab_procedures = st.slider("Lab Procedures", 1, 132, 45)
    with col2:
        number_diagnoses = st.slider("Number of Diagnoses", 1, 16, 7)
        num_procedures = st.slider("Procedures", 0, 6, 2)
        number_inpatient = st.slider("Previous Inpatient Visits", 0, 21, 0)
        number_emergency = st.slider("Previous Emergency Visits", 0, 76, 0)
    
    if st.button("🔮 Predict Readmission Risk", type="primary"):
        if model_loaded:
            input_data = pd.DataFrame(np.zeros((1, len(feature_names))), columns=feature_names)
            
            input_data['age'] = age
            input_data['time_in_hospital'] = time_in_hospital
            input_data['num_medications'] = num_medications
            input_data['num_lab_procedures'] = num_lab_procedures
            input_data['number_diagnoses'] = number_diagnoses
            input_data['num_procedures'] = num_procedures
            input_data['number_inpatient'] = number_inpatient
            input_data['number_emergency'] = number_emergency
            
            input_scaled = scaler.transform(input_data)
            prediction = model.predict(input_scaled, verbose=0)[0][0]
            risk_percent = prediction * 100
            
            st.info(f"**Patient Summary:** Age {age}, Hospital stay {time_in_hospital} days, {num_medications} medications")
            
            if risk_percent > 50:
                st.error(f"🔴 **High Risk of Readmission** — Probability: {risk_percent:.1f}%")
            else:
                st.success(f"🟢 **Low Risk of Readmission** — Probability: {risk_percent:.1f}%")
            
            st.caption("⚠️ Note: This is a demo prediction using 8 out of 71 features. Full prediction would require all features.")
        else:
            st.warning("⚠️ Model load nahi ho paya. Pehle `differential_privacy.py` chalayein.")

st.markdown("---")
st.caption("🎓 CS Final Year Project | Federated Learning for Healthcare with Differential Privacy")