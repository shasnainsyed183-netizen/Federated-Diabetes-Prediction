import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime
from chatbot import HealthChatbot
from chat_page import render_chat_page, render_floating_chatbot
from pdf_generator import generate_medical_report
import history_db as hist
import auth
from login_page import render_login_page, logout
from info_pages import render_email_page, render_website_page


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
# AUTHENTICATION CHECK
# ========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None

if not st.session_state.logged_in:
    render_login_page()
    st.stop()


# ========================================
# INFO PAGES SWITCHING (Email / Website)
# ========================================
if 'show_email_page' not in st.session_state:
    st.session_state.show_email_page = False
if 'show_website_page' not in st.session_state:
    st.session_state.show_website_page = False

if st.session_state.show_email_page:
    render_email_page()
    st.stop()

if st.session_state.show_website_page:
    render_website_page()
    st.stop()


# ========================================
# PAGE SWITCHING (Dashboard vs Chat)
# ========================================
if 'show_chat_page' not in st.session_state:
    st.session_state.show_chat_page = False

if st.session_state.show_chat_page:
    render_chat_page()
    st.stop()


# ========================================
# LAZY MODEL LOADING
# ========================================
@st.cache_resource(show_spinner=False)
def load_diabetes_model():
    import tensorflow as tf
    try:
        return {
            'model': tf.keras.models.load_model('federated_dp_model.keras'),
            'scaler': pickle.load(open('scaler.pkl', 'rb')),
            'features': pickle.load(open('feature_names.pkl', 'rb'))
        }
    except Exception as e:
        return None


@st.cache_resource(show_spinner=False)
def load_heart_model():
    import tensorflow as tf
    try:
        return {
            'model': tf.keras.models.load_model('heart_dp_model.keras'),
            'scaler': pickle.load(open('scaler_heart.pkl', 'rb')),
            'features': pickle.load(open('feature_names_heart.pkl', 'rb'))
        }
    except Exception as e:
        return None


@st.cache_resource(show_spinner=False)
def load_stroke_model():
    import tensorflow as tf
    try:
        return {
            'model': tf.keras.models.load_model('stroke_dp_model.keras'),
            'scaler': pickle.load(open('scaler_stroke.pkl', 'rb')),
            'features': pickle.load(open('feature_names_stroke.pkl', 'rb'))
        }
    except Exception as e:
        return None


def predict_with_model(model_dict, data_dict):
    if model_dict is None:
        return None
    m = model_dict
    input_df = pd.DataFrame(np.zeros((1, len(m['features']))), columns=m['features'])
    for key, val in data_dict.items():
        if key in input_df.columns:
            input_df[key] = val
    input_scaled = m['scaler'].transform(input_df)
    return float(m['model'].predict(input_scaled, verbose=0)[0][0])


# ========================================
# CUSTOM CSS
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
    
    .user-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        border: 1px solid rgba(102, 126, 234, 0.4);
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 10px;
        text-align: center;
    }
    
    .user-avatar {
        font-size: 2rem;
        margin-bottom: 6px;
    }
    
    .user-name {
        color: #ffffff;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 3px;
    }
    
    .user-email {
        color: #a0a0b0;
        font-size: 0.75rem;
        margin-bottom: 4px;
    }
    
    .user-hospital {
        color: #667eea;
        font-size: 0.7rem;
        font-weight: 500;
    }
    
    .contact-card {
        background: linear-gradient(135deg, #1e1e2e 0%, #2a2a3e 100%);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    
    .contact-card:hover {
        border-color: rgba(102, 126, 234, 0.6);
        transform: translateY(-3px);
    }
    
    .contact-card .contact-icon {
        font-size: 1.8rem;
        margin-bottom: 8px;
    }
    
    .contact-card .contact-title {
        color: #ffffff;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 5px;
    }
    
    .contact-card .contact-info {
        color: #b0b0c0;
        font-size: 0.88rem;
        line-height: 1.6;
    }
    
    .contact-card .contact-info strong {
        color: #10b981;
        font-size: 1rem;
    }
    
    .emergency-badge {
        display: inline-block;
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        padding: 3px 10px;
        border-radius: 8px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .gallery-card {
        background: linear-gradient(135deg, #1e1e2e 0%, #2a2a3e 100%);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 14px;
        overflow: hidden;
        margin-bottom: 20px;
        transition: all 0.35s ease;
        height: 100%;
    }
    
    .gallery-card:hover {
        border-color: rgba(102, 126, 234, 0.7);
        transform: translateY(-6px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.3);
    }
    
    .gallery-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        display: block;
    }
    
    .gallery-body {
        padding: 18px 20px 22px 20px;
    }
    
    .gallery-category {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        background: rgba(102, 126, 234, 0.15);
        color: #667eea;
        margin-bottom: 10px;
    }
    
    .gallery-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 8px;
    }
    
    .gallery-desc {
        font-size: 0.88rem;
        color: #b0b0c0;
        line-height: 1.5;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px !important;
        background: rgba(255, 255, 255, 0.03) !important;
        padding: 6px !important;
        border-radius: 12px !important;
        border-bottom: none !important;
        flex-wrap: wrap !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 44px !important;
        padding: 0 22px !important;
        border-radius: 10px !important;
        background: transparent !important;
        color: #b0b0c0 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
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
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3) !important;
        transition: all 0.25s ease !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.45) !important;
    }
    
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
# HERO HEADER
# ========================================
current_user = st.session_state.user
is_patient = current_user.get('role') == 'patient'
role_label = "Patient" if is_patient else "Doctor"

st.markdown(f"""
<div class="hero-header">
    <div class="hero-badge">🏆 Final Year Project 2026</div>
    <h1 class="hero-title">🏥 MediFederate</h1>
    <p class="hero-subtitle">
        Welcome, <strong>{current_user['full_name']}</strong> ({role_label}) · 
        Privacy-Preserving Multi-Disease Prediction Platform
    </p>
</div>
""", unsafe_allow_html=True)


# ========================================
# SIDEBAR
# ========================================
with st.sidebar:
    if is_patient:
        st.markdown("""
        <div class="user-card">
            <div class="user-avatar">👤</div>
            <div class="user-name">Patient Mode</div>
            <div class="user-email">Guest Access</div>
            <div class="user-hospital">🏥 No Login Required</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔐  Login as Doctor", use_container_width=True, key="switch_to_doctor"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.show_chat_page = False
            st.rerun()
    else:
        st.markdown(f"""
        <div class="user-card">
            <div class="user-avatar">👨‍⚕️</div>
            <div class="user-name">{current_user['full_name']}</div>
            <div class="user-email">{current_user['email']}</div>
            <div class="user-hospital">🏥 {current_user.get('hospital', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪  Logout", use_container_width=True, key="logout_btn"):
            logout()
    
    st.markdown("---")
    
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
    
    st.markdown("### 📞 Quick Helpline")
    st.markdown("""
    - 🚨 **Emergency:** 1122
    - 🚑 **Edhi:** 115
    """)
    
    col_e, col_w = st.columns(2)
    with col_e:
        if st.button("📧 Email", use_container_width=True, key="sidebar_email"):
            st.session_state.show_email_page = True
            st.rerun()
    with col_w:
        if st.button("🌐 Website", use_container_width=True, key="sidebar_website"):
            st.session_state.show_website_page = True
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 🛠️ Technology Stack")
    st.markdown("""
    - 🤖 **Federated Learning**
    - 🔒 **Differential Privacy**
    - 🧠 **Deep Neural Networks**
    - 🔍 **Explainable AI (SHAP)**
    - 💬 **AI Health Chatbot (Groq)**
    - 📄 **PDF Report Generation**
    - 📜 **Prediction History (SQLite)**
    - 🔐 **User Authentication**
    """)


# ========================================
# MAIN TABS (Role-based)
# ========================================
if is_patient:
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Overview",
        "🩸 Diabetes",
        "❤️ Heart Disease",
        "🧠 Stroke",
        "🏥 Gallery",
        "📞 Contacts"
    ])
    tab7 = None
else:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📈 Overview",
        "🩸 Diabetes",
        "❤️ Heart Disease",
        "🧠 Stroke",
        "🏥 Gallery",
        "📞 Contacts",
        "📜 History"
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
    
    if st.button("🔮 Predict Diabetes Risk", type="primary", key="d_btn"):
        with st.spinner("Loading model..."):
            model = load_diabetes_model()
        
        data = {
            'age': age, 'time_in_hospital': time_hosp,
            'num_medications': meds, 'num_lab_procedures': lab,
            'number_diagnoses': diag, 'num_procedures': proc,
            'number_inpatient': inpat, 'number_emergency': emerg,
        }
        
        prob = predict_with_model(model, data)
        
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
            
            hist.save_prediction(
                "Diabetes", prob,
                "High Risk" if prob > 0.5 else "Low Risk",
                f"Age: {age}, Time: {time_hosp}d, Meds: {meds}, Lab: {lab}, Diag: {diag}"
            )
            
            pdf_bytes = generate_medical_report(
                "Diabetes",
                {
                    "Age": age,
                    "Time in Hospital (days)": time_hosp,
                    "Number of Medications": meds,
                    "Lab Procedures": lab,
                    "Number of Diagnoses": diag,
                    "Procedures": proc,
                    "Previous Inpatient Visits": inpat,
                    "Previous Emergency Visits": emerg,
                },
                {
                    "probability": prob,
                    "is_high_risk": prob > 0.5,
                    "summary": f"Patient has {pct:.1f}% probability of readmission.",
                }
            )
            st.download_button(
                label="📄  Download PDF Report",
                data=pdf_bytes,
                file_name=f"MediFederate_Diabetes_Report_{age}y_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="d_download_btn"
            )
        else:
            st.error("⚠️ Diabetes model not loaded.")


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
        cp_h = st.slider("Chest Pain Type", 0, 3, 1, key="h_cp")
        trestbps = st.slider("Resting BP (mm Hg)", 90, 200, 130, key="h_bp")
        chol = st.slider("Cholesterol (mg/dl)", 100, 600, 240, key="h_chol")
        fbs = st.selectbox("Fasting Blood Sugar > 120", ["No", "Yes"], key="h_fbs")
    with col2:
        restecg = st.slider("Resting ECG", 0, 2, 1, key="h_ecg")
        thalach = st.slider("Max Heart Rate", 70, 210, 150, key="h_hr")
        exang = st.selectbox("Exercise Induced Angina", ["No", "Yes"], key="h_exang")
        oldpeak = st.slider("ST Depression", 0.0, 7.0, 1.0, key="h_old")
        slope = st.slider("Slope", 0, 2, 1, key="h_slope")
        ca = st.slider("Major Vessels (0-3)", 0, 3, 0, key="h_ca")
        thal = st.selectbox("Thalassemia", [1, 2, 3], key="h_thal")
    
    if st.button("🔮 Predict Heart Disease", type="primary", key="h_btn"):
        with st.spinner("Loading model..."):
            model = load_heart_model()
        
        data = {
            'age': age_h, 'sex': 1.0 if sex_h == "Male" else 0.0,
            'cp': float(cp_h), 'trestbps': float(trestbps), 'chol': float(chol),
            'fbs': 1.0 if fbs == "Yes" else 0.0, 'restecg': float(restecg),
            'thalach': float(thalach), 'exang': 1.0 if exang == "Yes" else 0.0,
            'oldpeak': float(oldpeak), 'slope': float(slope),
            'ca': float(ca), 'thal': float(thal),
        }
        
        prob = predict_with_model(model, data)
        
        if prob is not None:
            st.info(f"**Patient Summary:** Age {age_h} · {sex_h} · BP {trestbps} · Chol {chol}")
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
            
            hist.save_prediction(
                "Heart Disease", prob,
                "High Risk" if prob > 0.5 else "Low Risk",
                f"Age: {age_h}, {sex_h}, BP: {trestbps}, Chol: {chol}, MaxHR: {thalach}"
            )
            
            pdf_bytes = generate_medical_report(
                "Heart Disease",
                {
                    "Age": age_h,
                    "Gender": sex_h,
                    "Chest Pain Type": cp_h,
                    "Resting BP (mm Hg)": trestbps,
                    "Cholesterol (mg/dl)": chol,
                    "Fasting Blood Sugar > 120": fbs,
                    "Resting ECG": restecg,
                    "Max Heart Rate": thalach,
                    "Exercise Induced Angina": exang,
                    "ST Depression": oldpeak,
                    "Slope": slope,
                    "Major Vessels": ca,
                    "Thalassemia": thal,
                },
                {
                    "probability": prob,
                    "is_high_risk": prob > 0.5,
                    "summary": f"Patient has {pct:.1f}% probability of heart disease.",
                }
            )
            st.download_button(
                label="📄  Download PDF Report",
                data=pdf_bytes,
                file_name=f"MediFederate_Heart_Report_{age_h}y_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="h_download_btn"
            )
        else:
            st.error("⚠️ Heart model not loaded.")


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
        with st.spinner("Loading model..."):
            model = load_stroke_model()
        
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
        
        for wt in ['Never_worked', 'Private', 'Self-employed', 'children']:
            data[f'work_type_{wt}'] = 1.0 if work == wt else 0.0
        
        prob = predict_with_model(model, data)
        
        if prob is not None:
            st.info(f"**Patient Summary:** Age {age_s} · {gender_s} · Glucose {glucose} · BMI {bmi}")
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
            
            hist.save_prediction(
                "Stroke", prob,
                "High Risk" if prob > 0.5 else "Low Risk",
                f"Age: {age_s}, {gender_s}, Glucose: {glucose}, BMI: {bmi}, Smoking: {smoking}"
            )
            
            pdf_bytes = generate_medical_report(
                "Stroke",
                {
                    "Age": age_s,
                    "Gender": gender_s,
                    "Hypertension": hyp,
                    "Heart Disease": heart,
                    "Ever Married": married,
                    "Average Glucose Level": glucose,
                    "BMI": bmi,
                    "Work Type": work,
                    "Residence": residence,
                    "Smoking Status": smoking,
                },
                {
                    "probability": prob,
                    "is_high_risk": prob > 0.5,
                    "summary": f"Patient has {pct:.1f}% probability of stroke.",
                }
            )
            st.download_button(
                label="📄  Download PDF Report",
                data=pdf_bytes,
                file_name=f"MediFederate_Stroke_Report_{age_s}y_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="s_download_btn"
            )
        else:
            st.error("⚠️ Stroke model not loaded.")


# ========================================
# TAB 5: GALLERY
# ========================================
with tab5:
    st.markdown('<div class="section-header">🏥 Medical Knowledge Gallery</div>', unsafe_allow_html=True)
    st.markdown("""
    Explore important health conditions, their symptoms, and prevention tips. 
    Click on any card to learn more via **MediBot** 💬
    """)
    
    gallery_items = [
        {"category": "CARDIOLOGY", "title": "Blood Pressure Monitoring", "desc": "High BP is a silent killer. Get checked regularly — normal is 120/80 mm Hg. Reduce salt, exercise daily, manage stress.", "image": "https://images.unsplash.com/photo-1579154204601-01588f351e67?w=800&auto=format&fit=crop", "emoji": "💓", "query": "My blood pressure is high, what should I do?"},
        {"category": "CARDIOLOGY", "title": "Heart Health", "desc": "Cardiovascular disease is the #1 cause of death globally. Watch cholesterol, avoid smoking, and stay active.", "image": "https://images.unsplash.com/photo-1628348070889-cb656235b4eb?w=800&auto=format&fit=crop", "emoji": "❤️", "query": "I have chest pain, what should I do?"},
        {"category": "ENDOCRINOLOGY", "title": "Diabetes & Blood Sugar", "desc": "Over 537M adults live with diabetes. Watch for excessive thirst, frequent urination, and fatigue. Monitor sugar levels regularly.", "image": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=800&auto=format&fit=crop", "emoji": "🩸", "query": "My sugar level is 200, what should I do?"},
        {"category": "NEUROLOGY", "title": "Stroke Awareness", "desc": "Remember FAST: Face drooping, Arm weakness, Speech difficulty, Time to call 1122. Every minute counts!", "image": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&auto=format&fit=crop", "emoji": "🧠", "query": "Tell me about stroke symptoms"},
        {"category": "GENERAL HEALTH", "title": "Fever & Infections", "desc": "Fever is the body's defense against infection. Stay hydrated, rest well, and use paracetamol. Seek help if fever lasts 3+ days.", "image": "https://images.unsplash.com/photo-1584362917165-526a968579e8?w=800&auto=format&fit=crop", "emoji": "🌡️", "query": "I have fever, what should I do?"},
        {"category": "GASTROENTEROLOGY", "title": "Stomach & Digestion", "desc": "Avoid spicy, oily food. Eat smaller meals. Manage stress. If pain persists over 24 hours, see a doctor.", "image": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=800&auto=format&fit=crop", "emoji": "🤢", "query": "I have stomach pain, what should I do?"},
        {"category": "HEMATOLOGY", "title": "Blood Health", "desc": "Regular blood tests help detect anemia, infections, and other conditions early. Get checked every 6 months.", "image": "https://images.unsplash.com/photo-1631815589968-fdb09a223b1e?w=800&auto=format&fit=crop", "emoji": "🩸", "query": "I am feeling weakness, what should I do?"},
        {"category": "PHARMACOLOGY", "title": "Medication Safety", "desc": "Never self-medicate. Take antibiotics only when prescribed. Complete the full course. Store medicines properly.", "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800&auto=format&fit=crop", "emoji": "💊", "query": "How should I take my medicines?"},
        {"category": "PREVENTIVE CARE", "title": "Regular Checkups", "desc": "Annual health checkups catch problems early. BP, sugar, cholesterol, and full-body screening every year.", "image": "https://images.unsplash.com/photo-1584982751601-97dcc096659c?w=800&auto=format&fit=crop", "emoji": "🩺", "query": "How often should I get a health checkup?"},
        {"category": "EMERGENCY", "title": "Emergency Response", "desc": "Save these numbers: Rescue 1122, Edhi 115, Police 15, Chhipa 1020. In emergency, stay calm and call for help.", "image": "https://images.unsplash.com/photo-1587745416684-47953f16f02f?w=800&auto=format&fit=crop", "emoji": "🚨", "query": "What is the emergency number in Pakistan?"},
    ]
    
    for i in range(0, len(gallery_items), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            item = gallery_items[i]
            st.markdown(f"""
            <div class="gallery-card">
                <img src="{item['image']}" class="gallery-image" onerror="this.style.display='none'"/>
                <div class="gallery-body">
                    <span class="gallery-category">{item['category']}</span>
                    <div class="gallery-title">{item['emoji']} {item['title']}</div>
                    <div class="gallery-desc">{item['desc']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"💬 Ask MediBot about {item['title']}", key=f"gal_btn_{i}", use_container_width=True):
                st.session_state.show_chat_page = True
                st.session_state.pending_chat_query = item['query']
                st.rerun()
        
        with col2:
            if i + 1 < len(gallery_items):
                item = gallery_items[i + 1]
                st.markdown(f"""
                <div class="gallery-card">
                    <img src="{item['image']}" class="gallery-image" onerror="this.style.display='none'"/>
                    <div class="gallery-body">
                        <span class="gallery-category">{item['category']}</span>
                        <div class="gallery-title">{item['emoji']} {item['title']}</div>
                        <div class="gallery-desc">{item['desc']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"💬 Ask MediBot about {item['title']}", key=f"gal_btn_{i+1}", use_container_width=True):
                    st.session_state.show_chat_page = True
                    st.session_state.pending_chat_query = item['query']
                    st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 **Tip:** Har card ke neeche 'Ask MediBot' button dabayein — AI foran us topic par tafseel se jawab dega!")


# ========================================
# TAB 6: CONTACTS & HELPLINE
# ========================================
with tab6:
    st.markdown('<div class="section-header">📞 Contacts & Helpline</div>', unsafe_allow_html=True)
    st.markdown("""
    Emergency numbers, hospital contacts, and online support — sab kuch ek jagah.
    """)
    
    st.markdown("##### 🚨 Emergency Numbers")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="contact-card">
            <div class="emergency-badge">Emergency</div>
            <div class="contact-icon">🚨</div>
            <div class="contact-title">Rescue</div>
            <div class="contact-info"><strong>1122</strong></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="contact-card">
            <div class="emergency-badge">Ambulance</div>
            <div class="contact-icon">🚑</div>
            <div class="contact-title">Edhi Ambulance</div>
            <div class="contact-info"><strong>115</strong></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="contact-card">
            <div class="emergency-badge">Police</div>
            <div class="contact-icon">👮</div>
            <div class="contact-title">Police</div>
            <div class="contact-info"><strong>15</strong></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="contact-card">
            <div class="emergency-badge">Ambulance</div>
            <div class="contact-icon">🚑</div>
            <div class="contact-title">Chhipa</div>
            <div class="contact-info"><strong>1020</strong></div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("##### 🏥 Major Hospitals in Pakistan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="contact-card">
            <div class="contact-icon">🏥</div>
            <div class="contact-title">Aga Khan University Hospital</div>
            <div class="contact-info">
                📍 Karachi<br>
                📞 +92-21-111-911-911<br>
                🌐 hospitals.aku.edu
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="contact-card">
            <div class="contact-icon">🏥</div>
            <div class="contact-title">Mayo Hospital</div>
            <div class="contact-info">
                📍 Lahore<br>
                📞 +92-42-99211112<br>
                🌐 mayo-hospital.gov.pk
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="contact-card">
            <div class="contact-icon">🏥</div>
            <div class="contact-title">PIMS Islamabad</div>
            <div class="contact-info">
                📍 Islamabad<br>
                📞 +92-51-9261170<br>
                🌐 pims.gov.pk
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="contact-card">
            <div class="contact-icon">🏥</div>
            <div class="contact-title">Shaukat Khanum Memorial Hospital</div>
            <div class="contact-info">
                📍 Lahore & Peshawar<br>
                📞 +92-42-35905000<br>
                🌐 shaukatkhanum.org.pk
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="contact-card">
            <div class="contact-icon">🏥</div>
            <div class="contact-title">Jinnah Postgraduate Medical Centre</div>
            <div class="contact-info">
                📍 Karachi<br>
                📞 +92-21-99201300<br>
                🌐 jpmc.edu.pk
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="contact-card">
            <div class="contact-icon">🏥</div>
            <div class="contact-title">Services Hospital Lahore</div>
            <div class="contact-info">
                📍 Lahore<br>
                📞 +92-42-99203402<br>
                🌐 serviceshospital.punjab.gov.pk
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("##### 💬 MediFederate Support")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="contact-card">
            <div class="contact-icon">📞</div>
            <div class="contact-title">Helpline</div>
            <div class="contact-info"><strong>042-111-222-333</strong><br>Mon-Fri, 9 AM - 6 PM</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="contact-card">
            <div class="contact-icon">📧</div>
            <div class="contact-title">Email Support</div>
            <div class="contact-info"><strong>support@medifederate.com</strong><br>Response within 24 hours</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="contact-card">
            <div class="contact-icon">💬</div>
            <div class="contact-title">AI Chatbot</div>
            <div class="contact-info"><strong>MediBot</strong><br>Available 24/7 in-app</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("##### 🌐 Online Health Resources")
    st.markdown("""
    - **WHO Pakistan:** [www.emro.who.int/countries/pak](https://www.emro.who.int/countries/pak)
    - **NHSRC Pakistan:** [www.nhsrc.gov.pk](https://www.nhsrc.gov.pk)
    - **Health Ministry:** [www.nhrm.gov.pk](https://www.nhrm.gov.pk)
    - **MediFederate Website:** [www.medifederate.com](https://www.medifederate.com)
    """)


# ========================================
# TAB 7: HISTORY (Doctor Only)
# ========================================
if tab7 is not None:
    with tab7:
        st.markdown('<div class="section-header">📜 Prediction History</div>', unsafe_allow_html=True)
        st.markdown("""
        Saari AI predictions yahan save hain. Aap filter, export, aur analytics dekh sakte hain.
        """)
        
        stats = hist.get_statistics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem;">📊</div>
                <div class="metric-label">Total Predictions</div>
                <div class="metric-value">{stats['total']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem;">🔴</div>
                <div class="metric-label">High Risk</div>
                <div class="metric-value" style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">{stats['high_risk']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem;">🟢</div>
                <div class="metric-label">Low Risk</div>
                <div class="metric-value" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">{stats['low_risk']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem;">🏥</div>
                <div class="metric-label">Diseases Covered</div>
                <div class="metric-value">3</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_f1, col_f2, col_f3 = st.columns([2, 2, 1])
        
        with col_f1:
            disease_filter = st.selectbox(
                "🔍 Filter by Disease",
                ["All", "Diabetes", "Heart Disease", "Stroke"],
                key="hist_filter"
            )
        
        with col_f2:
            st.markdown("&nbsp;")
            csv_data = hist.export_to_csv()
            st.download_button(
                label="📥  Export to CSV",
                data=csv_data,
                file_name=f"MediFederate_History_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True,
                key="hist_export"
            )
        
        with col_f3:
            st.markdown("&nbsp;")
            if st.button("🗑️  Clear All", use_container_width=True, key="hist_clear"):
                hist.clear_all_predictions()
                st.success("All history cleared!")
                st.rerun()
        
        st.markdown("---")
        
        st.markdown("##### 📊 Analytics")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("**Disease Distribution**")
            disease_dist = hist.get_disease_distribution()
            if not disease_dist.empty:
                st.bar_chart(disease_dist.set_index('disease')['count'], height=250)
            else:
                st.info("No data yet")
        
        with col_chart2:
            st.markdown("**Risk Distribution**")
            risk_dist = hist.get_risk_distribution()
            if not risk_dist.empty:
                st.bar_chart(risk_dist.set_index('risk_level')['count'], height=250)
            else:
                st.info("No data yet")
        
        st.markdown("---")
        
        st.markdown("##### 📋 All Predictions")
        
        df = hist.get_all_predictions(disease_filter=disease_filter)
        
        if not df.empty:
            display_df = df[['id', 'timestamp', 'disease', 'probability', 'risk_level']].copy()
            display_df['probability'] = (display_df['probability'] * 100).round(1).astype(str) + '%'
            display_df.columns = ['ID', 'Timestamp', 'Disease', 'Probability', 'Risk Level']
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            st.markdown("##### 🔍 View Details")
            
            selected_id = st.selectbox(
                "Select Prediction ID to view details:",
                df['id'].tolist(),
                key="hist_detail"
            )
            
            if selected_id:
                row = df[df['id'] == selected_id].iloc[0]
                
                col_d1, col_d2 = st.columns(2)
                
                with col_d1:
                    st.markdown(f"""
                    **Prediction #{row['id']}**
                    - 🕐 **Time:** {row['timestamp']}
                    - 🏥 **Disease:** {row['disease']}
                    - 📊 **Probability:** {row['probability']*100:.1f}%
                    - 🎯 **Risk Level:** {row['risk_level']}
                    """)
                
                with col_d2:
                    st.markdown("**Patient Data:**")
                    st.code(row['patient_data'], language="python")
                
                if st.button(f"🗑️  Delete Prediction #{selected_id}", key="hist_del_one"):
                    hist.delete_prediction(selected_id)
                    st.success(f"Prediction #{selected_id} deleted!")
                    st.rerun()
        else:
            st.info("📭 No predictions yet. Go to Diabetes, Heart, or Stroke tab to make a prediction!")


# ========================================
# FLOATING WIDGET
# ========================================
render_floating_chatbot()


# ========================================
# FOOTER
# ========================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 20px 0; color: #808090;">
    <p style="margin: 0; font-size: 0.9rem;">
        🎓 <strong>CS Final Year Project 2026</strong> · MediFederate Platform v2.0
    </p>
    <p style="margin: 5px 0 0 0; font-size: 0.8rem;">
        Logged in as: <strong>{current_user['full_name']}</strong> ({role_label}) · 
        Federated Learning · Differential Privacy · Explainable AI
    </p>
</div>
""", unsafe_allow_html=True)