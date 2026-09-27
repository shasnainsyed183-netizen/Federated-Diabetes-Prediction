import streamlit as st
import pandas as pd
import numpy as np
import pickle
import tensorflow as tf
import os
from chatbot import HealthChatbot
from chat_page import render_chat_page, render_floating_chatbot


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
# PAGE SWITCHING (Dashboard vs Chat)
# ========================================
if 'show_chat_page' not in st.session_state:
    st.session_state.show_chat_page = False

if st.session_state.show_chat_page:
    render_chat_page()
    st.stop()


# ========================================
# CUSTOM CSS - Professional Theme
# ========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
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
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin: 30px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(102, 126, 234, 0.3);
    }
    
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
    .pill-danger { background: rgba(239, 68, 68, 0.15); color: #ef4444; }
    
    /* Navigation Card in Sidebar */
    .nav-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 10px;
    }
    
    .nav-card-title {
        color: #ffffff;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 10px;
    }
    
    .nav-item-active {
        color: #667eea;
        font-size: 0.9rem;
        font-weight: 600;
        padding: 6px 0;
    }
    
    /* CLEAN TABS */
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
    
    .stTabs [data-baseweb="tab-highlight"] {
        background: transparent !important;
        display: none !important;
    }
    
    .stTabs [data-baseweb="tab-border"] {
        background: transparent !important;
        display: none !important;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
    }
    
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
    
    /* Result box */
    .result-box {
        padding: 20px;
        border-radius: 12px;
        margin-top: 15px;
        border-left: 5px solid;
    }
    
    .result-high {
        background: rgba(239, 68, 68, 0.1);
        border-left-color: #ef4444;
    }
    
    .result-low {
        background: rgba(16, 185, 129, 0.1);
        border-left-color: #10b981;
    }
    
    .result-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .result-prob {
        font-size: 2rem;
        font-weight: 800;
        margin: 8px 0;
    }
    
    .result-desc {
        font-size: 0.9rem;
        color: #b0b0c0;
    }
</style>
""", unsafe_allow_html=True)


# ========================================
# LOAD MODELS & PREPROCESSORS
# ========================================
@st.cache_resource
def load_all_models():
    """Load all 3 models and their preprocessors"""
    models = {}
    
    try:
        models['diabetes'] = {
            'model': tf.keras.models.load_model('federated_dp_model.keras'),
            'scaler': pickle.load(open('scaler.pkl', 'rb')),
            'features': pickle.load(open('feature_names.pkl', 'rb'))
        }
    except Exception as e:
        models['diabetes'] = None
        st.warning(f"Diabetes model not loaded: {e}")
    
    try:
        models['heart'] = {
            'model': tf.keras.models.load_model('heart_dp_model.keras'),
            'scaler': pickle.load(open('scaler_heart.pkl', 'rb')),
            'features': pickle.load(open('feature_names_heart.pkl', 'rb'))
        }
    except Exception as e:
        models['heart'] = None
        st.warning(f"Heart model not loaded: {e}")
    
    try:
        models['stroke'] = {
            'model': tf.keras.models.load_model('stroke_dp_model.keras'),
            'scaler': pickle.load(open('scaler_stroke.pkl', 'rb')),
            'features': pickle.load(open('feature_names_stroke.pkl', 'rb'))
        }
    except Exception as e:
        models['stroke'] = None
        st.warning(f"Stroke model not loaded: {e}")
    
    return models


with st.spinner("Loading AI models..."):
    MODELS = load_all_models()


def predict_heart(data_dict):
    if MODELS['heart'] is None:
        return None
    m = MODELS['heart']
    input_df = pd.DataFrame(np.zeros((1, len(m['features']))), columns=m['features'])
    for key, val in data_dict.items():
        if key in input_df.columns:
            input_df[key] = val
    input_scaled = m['scaler'].transform(input_df)
    return float(m['model'].predict(input_scaled, verbose=0)[0][0])


def predict_stroke(data_dict):
    if MODELS['stroke'] is None:
        return None
    m = MODELS['stroke']
    input_df = pd.DataFrame(np.zeros((1, len(m['features']))), columns=m['features'])
    for key, val in data_dict.items():
        if key in input_df.columns:
            input_df[key] = val
    input_scaled = m['scaler'].transform(input_df)
    return float(m['model'].predict(input_scaled, verbose=0)[0][0])


def predict_diabetes(data_dict):
    if MODELS['diabetes'] is None:
        return None
    m = MODELS['diabetes']
    input_df = pd.DataFrame(np.zeros((1, len(m['features']))), columns=m['features'])
    for key, val in data_dict.items():
        if key in input_df.columns:
            input_df[key] = val
    input_scaled = m['scaler'].transform(input_df)
    return float(m['model'].predict(input_scaled, verbose=0)[0][0])


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
    # ===== NAVIGATION SECTION (TOP) =====
    st.markdown("""
    <div class="nav-card">
        <div class="nav-card-title">🧭 Navigation</div>
        <div class="nav-item-active">🏠 Dashboard (Current)</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("💬  Open MediBot Chat", use_container_width=True, type="primary", key="sidebar_open_chat"):
        st.session_state.show_chat_page = True
        st.rerun()
    
    st.markdown("---")
    
    # ===== BRANDING =====
    st.markdown("""
    <div style="text-align:center; padding: 10px 0 20px 0;">
        <div style="font-size: 2.5rem;">🏥</div>
        <h2 style="color: white; margin: 5px 0;">MediFederate</h2>
        <p style="color: #a0a0b0; font-size: 0.85rem; margin: 0;">v2.0 · 2026</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 Platform Stats")
    
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        if MODELS['diabetes']:
            st.success("🩸 Diabetes ✅")
        else:
            st.error("🩸 Diabetes ❌")
        if MODELS['heart']:
            st.success("❤️ Heart ✅")
        else:
            st.error("❤️ Heart ❌")
    with col_stat2:
        if MODELS['stroke']:
            st.success("🧠 Stroke ✅")
        else:
            st.error("🧠 Stroke ❌")
        st.info("📊 Real AI")
    
    st.markdown("---")
    st.markdown("### 🛠️ Technology Stack")
    st.markdown("""
    - 🤖 **Federated Learning**
    - 🔒 **Differential Privacy**
    - 🧠 **Deep Neural Networks**
    - 🔍 **Explainable AI (SHAP)**
    - 💬 **AI Health Chatbot**
    """)


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
    **without sharing any patient data**. All predictions are made using **real trained neural networks**.
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
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
    st.success("✅ **All predictions are powered by real trained neural networks** with Federated Learning + Differential Privacy — **ZERO patient data shared!**")


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
        st.metric("Model Status", "✅ Loaded" if MODELS['diabetes'] else "❌ Not Loaded")
    
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
    
    if st.button("🔮 Predict Diabetes Risk", type="primary", key="d_btn"):
        data = {
            'age': age,
            'time_in_hospital': time_hosp,
            'num_medications': meds,
            'num_lab_procedures': lab,
            'number_diagnoses': diag,
            'num_procedures': proc,
            'number_inpatient': inpat,
            'number_emergency': emerg,
        }
        
        prob = predict_diabetes(data)
        
        if prob is not None:
            st.info(f"**Patient Summary:** Age {age} · {time_hosp} days in hospital · {meds} medications")
            pct = prob * 100
            if prob > 0.5:
                st.markdown(f"""
                <div class="result-box result-high">
                    <div class="result-title">🔴 High Risk of Readmission</div>
                    <div class="result-prob">{pct:.1f}%</div>
                    <div class="result-desc">This patient has a high probability of being readmitted. Close monitoring is recommended.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-box result-low">
                    <div class="result-title">🟢 Low Risk of Readmission</div>
                    <div class="result-prob">{pct:.1f}%</div>
                    <div class="result-desc">This patient has a low probability of readmission. Standard follow-up is sufficient.</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("⚠️ Diabetes model not loaded. Please check `federated_dp_model.keras`")


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
        st.metric("Model Status", "✅ Loaded" if MODELS['heart'] else "❌ Not Loaded")
    
    st.markdown("---")
    st.markdown("#### Enter Patient Details")
    
    col1, col2 = st.columns(2)
    with col1:
        age_h = st.slider("Age", 20, 90, 55, key="h_age")
        sex_h = st.selectbox("Gender", ["Male", "Female"], key="h_sex")
        cp_h = st.slider("Chest Pain Type (0=typical, 1=atypical, 2=non-anginal, 3=asymptomatic)", 0, 3, 1, key="h_cp")
        trestbps = st.slider("Resting BP (mm Hg)", 90, 200, 130, key="h_bp")
        chol = st.slider("Cholesterol (mg/dl)", 100, 600, 240, key="h_chol")
        fbs = st.selectbox("Fasting Blood Sugar > 120", ["No", "Yes"], key="h_fbs")
    with col2:
        restecg = st.slider("Resting ECG (0=normal, 1=ST-T, 2=LVH)", 0, 2, 1, key="h_ecg")
        thalach = st.slider("Max Heart Rate", 70, 210, 150, key="h_hr")
        exang = st.selectbox("Exercise Induced Angina", ["No", "Yes"], key="h_exang")
        oldpeak = st.slider("ST Depression", 0.0, 7.0, 1.0, key="h_old")
        slope = st.slider("Slope (0=up, 1=flat, 2=down)", 0, 2, 1, key="h_slope")
        ca = st.slider("Major Vessels (0-3)", 0, 3, 0, key="h_ca")
        thal = st.selectbox("Thalassemia (1=normal, 2=fixed, 3=reversible)", [1, 2, 3], key="h_thal")
    
    if st.button("🔮 Predict Heart Disease", type="primary", key="h_btn"):
        data = {
            'age': age_h,
            'sex': 1.0 if sex_h == "Male" else 0.0,
            'cp': float(cp_h),
            'trestbps': float(trestbps),
            'chol': float(chol),
            'fbs': 1.0 if fbs == "Yes" else 0.0,
            'restecg': float(restecg),
            'thalach': float(thalach),
            'exang': 1.0 if exang == "Yes" else 0.0,
            'oldpeak': float(oldpeak),
            'slope': float(slope),
            'ca': float(ca),
            'thal': float(thal),
        }
        
        prob = predict_heart(data)
        
        if prob is not None:
            st.info(f"**Patient Summary:** Age {age_h} · {sex_h} · BP {trestbps} · Chol {chol} · MaxHR {thalach}")
            pct = prob * 100
            if prob > 0.5:
                st.markdown(f"""
                <div class="result-box result-high">
                    <div class="result-title">🔴 High Risk of Heart Disease</div>
                    <div class="result-prob">{pct:.1f}%</div>
                    <div class="result-desc">This patient shows signs of heart disease. Further cardiac evaluation is recommended.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-box result-low">
                    <div class="result-title">🟢 Low Risk of Heart Disease</div>
                    <div class="result-prob">{pct:.1f}%</div>
                    <div class="result-desc">This patient shows low risk for heart disease. Routine checkup is sufficient.</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("⚠️ Heart model not loaded. Please check `heart_dp_model.keras`")


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
        st.metric("Model Status", "✅ Loaded" if MODELS['stroke'] else "❌ Not Loaded")
    
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
        data = {
            'gender': 1.0 if gender_s == "Male" else 0.0,
            'age': float(age_s),
            'hypertension': 1.0 if hyp == "Yes" else 0.0,
            'heart_disease': 1.0 if heart == "Yes" else 0.0,
            'ever_married': 1.0 if married == "Yes" else 0.0,
            'Residence_type': 1.0 if residence == "Urban" else 0.0,
            'avg_glucose_level': float(glucose),
            'bmi': float(bmi),
            'smoking_status': {'never smoked': 0.0, 'formerly smoked': 1.0, 'smokes': 2.0, 'Unknown': 3.0}[smoking],
        }
        
        work_types = ['Never_worked', 'Private', 'Self-employed', 'children']
        for wt in work_types:
            data[f'work_type_{wt}'] = 1.0 if work == wt else 0.0
        
        prob = predict_stroke(data)
        
        if prob is not None:
            st.info(f"**Patient Summary:** Age {age_s} · {gender_s} · Glucose {glucose} · BMI {bmi} · {smoking}")
            pct = prob * 100
            if prob > 0.5:
                st.markdown(f"""
                <div class="result-box result-high">
                    <div class="result-title">🔴 High Risk of Stroke</div>
                    <div class="result-prob">{pct:.1f}%</div>
                    <div class="result-desc">This patient has a high risk of stroke. Immediate medical consultation is recommended.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-box result-low">
                    <div class="result-title">🟢 Low Risk of Stroke</div>
                    <div class="result-prob">{pct:.1f}%</div>
                    <div class="result-desc">This patient has a low risk of stroke. Maintain a healthy lifestyle.</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("⚠️ Stroke model not loaded. Please check `stroke_dp_model.keras`")


# ========================================
# FLOATING WIDGET
# ========================================
render_floating_chatbot()


# ========================================
# FOOTER
# ========================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px 0; color: #808090;">
    <p style="margin: 0; font-size: 0.9rem;">
        🎓 <strong>CS Final Year Project 2026</strong> · MediFederate Platform v2.0
    </p>
    <p style="margin: 5px 0 0 0; font-size: 0.8rem;">
        Federated Learning · Differential Privacy · Explainable AI · AI Chatbot · Real Neural Networks
    </p>
</div>
""", unsafe_allow_html=True)