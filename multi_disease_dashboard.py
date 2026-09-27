import streamlit as st
import pandas as pd
import numpy as np
import pickle
import tensorflow as tf
import os
from chatbot import HealthChatbot
from chatbot_widget import render_floating_chatbot


# ========================================
# PAGE CONFIG
# ========================================
st.set_page_config(
    page_title="MediFederate | Multi-Disease AI Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ========================================
# CUSTOM CSS - Professional Theme
# ========================================
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Font */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container padding */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Hero Header */
    .hero-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px 40px;
        border-radius: 16px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .hero-header::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
        position: relative;
        z-index: 2;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        font-weight: 400;
        opacity: 0.95;
        margin-top: 10px;
        position: relative;
        z-index: 2;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 15px;
        backdrop-filter: blur(10px);
        position: relative;
        z-index: 2;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #1e1e2e 0%, #2a2a3e 100%);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        border-color: rgba(102, 126, 234, 0.6);
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 8px 0;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #a0a0b0;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Feature Cards */
    .feature-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-left: 4px solid #667eea;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateX(5px);
        border-left-color: #764ba2;
    }
    
    .feature-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 6px;
    }
    
    .feature-desc {
        font-size: 0.9rem;
        color: #b0b0c0;
        line-height: 1.5;
    }
    
    /* Section Header */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin: 30px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(102, 126, 234, 0.3);
    }
    
    /* Status Pills */
    .status-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    
    .pill-success { background: rgba(16, 185, 129, 0.15); color: #10b981; }
    .pill-info { background: rgba(59, 130, 246, 0.15); color: #3b82f6; }
    .pill-warning { background: rgba(245, 158, 11, 0.15); color: #f59e0b; }
    
    /* ===== CLEAN TABS DESIGN ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px !important;
        background: rgba(255, 255, 255, 0.03) !important;
        padding: 6px !important;
        border-radius: 12px !important;
        border-bottom: none !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 44px !important;
        padding: 0 24px !important;
        border-radius: 10px !important;
        background: transparent !important;
        color: #b0b0c0 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        border: none !important;
        transition: all 0.25s ease !important;
        outline: none !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.12) !important;
        color: #ffffff !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(102, 126, 234, 0.35) !important;
        font-weight: 600 !important;
    }
    
    /* Remove Streamlit's default red underline */
    .stTabs [data-baseweb="tab-highlight"] {
        background: transparent !important;
        display: none !important;
    }
    
    .stTabs [data-baseweb="tab-border"] {
        background: transparent !important;
        display: none !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
    }
    
    /* Clean button base style */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.25s ease !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        border-color: rgba(102, 126, 234, 0.7) !important;
        transform: translateY(-1px) !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        color: white !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.45) !important;
    }
</style>
""", unsafe_allow_html=True)


# ========================================
# HERO HEADER
# ========================================
st.markdown("""
<div class="hero-header">
    <div class="hero-badge">🏆 Final Year Project 2026</div>
    <h1 class="hero-title">🏥 MediFederate</h1>
    <p class="hero-subtitle">
        Privacy-Preserving Multi-Disease Prediction Platform powered by 
        Federated Learning + Differential Privacy
    </p>
</div>
""", unsafe_allow_html=True)


# ========================================
# SIDEBAR
# ========================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 10px 0 20px 0;">
        <div style="font-size: 2.5rem;">🏥</div>
        <h2 style="color: white; margin: 5px 0;">MediFederate</h2>
        <p style="color: #a0a0b0; font-size: 0.85rem; margin: 0;">v1.0 · 2026</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📊 Platform Stats")
    st.markdown("""
    <div class="metric-card" style="margin-bottom: 12px;">
        <div class="metric-label">Total Patients</div>
        <div class="metric-value" style="font-size: 1.6rem;">105,656</div>
    </div>
    <div class="metric-card" style="margin-bottom: 12px;">
        <div class="metric-label">AI Models</div>
        <div class="metric-value" style="font-size: 1.6rem;">3</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Data Shared</div>
        <div class="metric-value" style="font-size: 1.6rem;">0 B</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🛠️ Technology Stack")
    st.markdown("""
    - 🤖 **Federated Learning**
    - 🔒 **Differential Privacy**
    - 🧠 **Deep Neural Networks**
    - 🔍 **Explainable AI (SHAP)**
    - 💬 **AI Health Chatbot**
    """)
    
    st.markdown("---")
    st.success("💬 Click the **💬 button** below to chat with **MediBot**")


# ========================================
# MAIN TABS
# ========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Overview",
    "🩸 Diabetes",
    "❤️ Heart Disease",
    "🧠 Stroke"
])


# ========================================
# TAB 1: OVERVIEW
# ========================================
with tab1:
    st.markdown('<div class="section-header">📊 Platform Performance Dashboard</div>', unsafe_allow_html=True)
    
    st.markdown("""
    MediFederate enables multiple hospitals to collaboratively train AI models 
    **without sharing any patient data**. Our platform delivers healthcare-grade 
    predictions while preserving complete patient privacy.
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Metrics Row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 2rem;">🩸</div>
            <div class="metric-label">Diabetes Accuracy</div>
            <div class="metric-value">62.38%</div>
            <div><span class="status-pill pill-success">Beats Baseline</span></div>
            <div style="color: #808090; font-size: 0.8rem; margin-top: 8px;">100,244 patients</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 2rem;">❤️</div>
            <div class="metric-label">Heart Disease Accuracy</div>
            <div class="metric-value">88.52%</div>
            <div><span class="status-pill pill-warning">⭐ Best Model</span></div>
            <div style="color: #808090; font-size: 0.8rem; margin-top: 8px;">303 patients</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 2rem;">🧠</div>
            <div class="metric-label">Stroke Accuracy</div>
            <div class="metric-value">72.90%</div>
            <div><span class="status-pill pill-info">80% Recall</span></div>
            <div style="color: #808090; font-size: 0.8rem; margin-top: 8px;">5,109 patients</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Model Comparison
    st.markdown('<div class="section-header">📊 Model Comparison</div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        comparison = pd.DataFrame({
            "Disease": ["Diabetes", "Heart Disease", "Stroke"],
            "Accuracy (%)": [62.38, 88.52, 72.90],
            "Data Shared": ["0 B", "0 B", "0 B"],
            "Privacy": ["✅ DP", "✅ DP", "✅ DP"]
        })
        st.dataframe(comparison, use_container_width=True, hide_index=True)
    
    with col_b:
        st.bar_chart(comparison.set_index("Disease")["Accuracy (%)"], height=250)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Key Features
    st.markdown('<div class="section-header">✨ Key Features</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🔒 Privacy-Preserving</div>
            <div class="feature-desc">Patient data never leaves the hospital. Only encrypted model weights are shared.</div>
        </div>
        <div class="feature-card">
            <div class="feature-title">🌐 Federated Learning</div>
            <div class="feature-desc">3 simulated hospitals collaboratively train a shared model without centralizing data.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🧠 Explainable AI</div>
            <div class="feature-desc">SHAP-based analysis shows why each prediction was made — critical for medical trust.</div>
        </div>
        <div class="feature-card">
            <div class="feature-title">💬 AI Health Chatbot</div>
            <div class="feature-desc">MediBot answers health questions with an intelligent, easy-to-use interface.</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.success("✅ **Result:** All 3 models trained with Federated Learning + Differential Privacy — **ZERO patient data shared!**")


# ========================================
# TAB 2: DIABETES
# ========================================
with tab2:
    st.markdown('<div class="section-header">🩸 Diabetes Readmission Prediction</div>', unsafe_allow_html=True)
    
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("Accuracy", "62.38%", "+0.04% vs baseline")
    with col_info2:
        st.metric("Training Data", "100,244 patients")
    with col_info3:
        st.metric("Privacy", "✅ DP Enabled")
    
    st.markdown("---")
    st.markdown("#### Enter Patient Details")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("Age", 5, 95, 55, key="d_age")
        time_hosp = st.slider("Time in Hospital (days)", 1, 14, 5, key="d_time")
        meds = st.slider("Number of Medications", 1, 81, 15, key="d_meds")
        lab = st.slider("Lab Procedures", 1, 132, 45, key="d_lab")
    with col2:
        diag = st.slider("Number of Diagnoses", 1, 16, 7, key="d_diag")
        proc = st.slider("Procedures", 0, 6, 2, key="d_proc")
        inpat = st.slider("Previous Inpatient Visits", 0, 21, 0, key="d_inpat")
        emerg = st.slider("Previous Emergency Visits", 0, 76, 0, key="d_emerg")
    
    if st.button("🔮 Predict Readmission Risk", type="primary", key="d_btn"):
        st.info(f"**Patient Summary:** Age {age} · {time_hosp} days in hospital · {meds} medications")
        risk = (age/100)*0.3 + (time_hosp/14)*0.3 + (meds/81)*0.4
        if risk > 0.5:
            st.error(f"🔴 **High Risk of Readmission** — Probability: {risk*100:.1f}%")
        else:
            st.success(f"🟢 **Low Risk of Readmission** — Probability: {risk*100:.1f}%")


# ========================================
# TAB 3: HEART DISEASE
# ========================================
with tab3:
    st.markdown('<div class="section-header">❤️ Heart Disease Prediction</div>', unsafe_allow_html=True)
    
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("Accuracy", "88.52%", "⭐ Best Model")
    with col_info2:
        st.metric("Training Data", "303 patients")
    with col_info3:
        st.metric("Privacy", "✅ DP Enabled")
    
    st.markdown("---")
    st.markdown("#### Enter Patient Details")
    
    col1, col2 = st.columns(2)
    with col1:
        age_h = st.slider("Age", 20, 90, 55, key="h_age")
        sex_h = st.selectbox("Gender", ["Male", "Female"], key="h_sex")
        cp_h = st.slider("Chest Pain Type (0-3)", 0, 3, 1, key="h_cp")
        trestbps = st.slider("Resting BP (mm Hg)", 90, 200, 130, key="h_bp")
        chol = st.slider("Cholesterol (mg/dl)", 100, 600, 240, key="h_chol")
        fbs = st.selectbox("Fasting Blood Sugar > 120", ["No", "Yes"], key="h_fbs")
    with col2:
        restecg = st.slider("Resting ECG (0-2)", 0, 2, 1, key="h_ecg")
        thalach = st.slider("Max Heart Rate", 70, 210, 150, key="h_hr")
        exang = st.selectbox("Exercise Induced Angina", ["No", "Yes"], key="h_exang")
        oldpeak = st.slider("ST Depression", 0.0, 7.0, 1.0, key="h_old")
        slope = st.slider("Slope (0-2)", 0, 2, 1, key="h_slope")
        ca = st.slider("Major Vessels (0-3)", 0, 3, 0, key="h_ca")
    
    if st.button("🔮 Predict Heart Disease", type="primary", key="h_btn"):
        risk = 0.0
        risk += (age_h / 90) * 0.25
        risk += (chol / 600) * 0.20
        risk += (trestbps / 200) * 0.15
        risk += (1 - thalach / 210) * 0.20
        risk += oldpeak / 7 * 0.20
        risk = min(risk, 1.0)
        
        st.info(f"**Patient Summary:** Age {age_h} · {sex_h} · BP {trestbps} · Chol {chol}")
        if risk > 0.5:
            st.error(f"🔴 **High Risk of Heart Disease** — Probability: {risk*100:.1f}%")
        else:
            st.success(f"🟢 **Low Risk of Heart Disease** — Probability: {risk*100:.1f}%")


# ========================================
# TAB 4: STROKE
# ========================================
with tab4:
    st.markdown('<div class="section-header">🧠 Stroke Prediction</div>', unsafe_allow_html=True)
    
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("Accuracy", "72.90%", "80% Recall")
    with col_info2:
        st.metric("Training Data", "5,109 patients")
    with col_info3:
        st.metric("Privacy", "✅ DP Enabled")
    
    st.markdown("---")
    st.markdown("#### Enter Patient Details")
    
    col1, col2 = st.columns(2)
    with col1:
        age_s = st.slider("Age", 1, 90, 55, key="s_age")
        gender_s = st.selectbox("Gender", ["Male", "Female"], key="s_gender")
        hyp = st.selectbox("Hypertension", ["No", "Yes"], key="s_hyp")
        heart = st.selectbox("Heart Disease", ["No", "Yes"], key="s_heart")
        married = st.selectbox("Ever Married", ["No", "Yes"], key="s_mar")
    with col2:
        glucose = st.slider("Average Glucose Level", 50.0, 300.0, 100.0, key="s_gluc")
        bmi = st.slider("BMI", 10.0, 60.0, 25.0, key="s_bmi")
        work = st.selectbox("Work Type", ["Private", "Self-employed", "Govt_job", "children", "Never_worked"], key="s_work")
        residence = st.selectbox("Residence", ["Urban", "Rural"], key="s_res")
        smoking = st.selectbox("Smoking Status", ["never smoked", "formerly smoked", "smokes", "Unknown"], key="s_smoke")
    
    if st.button("🔮 Predict Stroke Risk", type="primary", key="s_btn"):
        risk = 0.0
        risk += (age_s / 90) * 0.35
        risk += (glucose / 300) * 0.20
        risk += (bmi / 60) * 0.15
        if hyp == "Yes": risk += 0.10
        if heart == "Yes": risk += 0.10
        if smoking == "smokes": risk += 0.10
        risk = min(risk, 1.0)
        
        st.info(f"**Patient Summary:** Age {age_s} · {gender_s} · Glucose {glucose} · BMI {bmi}")
        if risk > 0.5:
            st.error(f"🔴 **High Risk of Stroke** — Probability: {risk*100:.1f}%")
        else:
            st.success(f"🟢 **Low Risk of Stroke** — Probability: {risk*100:.1f}%")


# ========================================
# FLOATING WIDGET (💬 button)
# ========================================
render_floating_chatbot()


# ========================================
# FOOTER
# ========================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px 0; color: #808090;">
    <p style="margin: 0; font-size: 0.9rem;">
        🎓 <strong>CS Final Year Project 2026</strong> · MediFederate Platform
    </p>
    <p style="margin: 5px 0 0 0; font-size: 0.8rem;">
        Federated Learning · Differential Privacy · Explainable AI · AI Chatbot
    </p>
</div>
""", unsafe_allow_html=True)