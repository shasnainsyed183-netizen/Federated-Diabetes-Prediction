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
from legal_pages import render_privacy_policy, render_terms_of_service
from settings_page import show_settings_dialog
import ui_helpers as ui


st.set_page_config(
    page_title="MediFederate | Multi-Disease AI Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ========================================
# INFO & LEGAL PAGES SWITCHING (BEFORE LOGIN)
# ========================================
if 'show_email_page' not in st.session_state:
    st.session_state.show_email_page = False
if 'show_website_page' not in st.session_state:
    st.session_state.show_website_page = False
if 'show_privacy_page' not in st.session_state:
    st.session_state.show_privacy_page = False
if 'show_terms_page' not in st.session_state:
    st.session_state.show_terms_page = False

if st.session_state.show_email_page:
    render_email_page()
    st.stop()

if st.session_state.show_website_page:
    render_website_page()
    st.stop()

if st.session_state.show_privacy_page:
    render_privacy_policy()
    st.stop()

if st.session_state.show_terms_page:
    render_terms_of_service()
    st.stop()


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
    except Exception:
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
    except Exception:
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
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def load_kidney_model():
    import tensorflow as tf
    try:
        return {
            'model': tf.keras.models.load_model('kidney_dp_model.keras'),
            'scaler': pickle.load(open('scaler_kidney.pkl', 'rb')),
            'features': pickle.load(open('feature_names_kidney.pkl', 'rb'))
        }
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def load_thyroid_model():
    import tensorflow as tf
    try:
        features = [
            'age', 'sex', 'TSH', 'T3', 'TT4', 'T4U', 'FTI', 
            'on_thyroxine', 'query_on_thyroxine', 'on_antithyroid_meds', 
            'sick', 'pregnant', 'thyroid_surgery', 'I131_treatment', 
            'query_hypothyroid', 'query_hyperthyroid', 'lithium', 
            'goitre', 'tumor', 'hypopituitary', 'psych', 
            'TSH_measured', 'T3_measured', 'TT4_measured', 
            'T4U_measured', 'FTI_measured', 'TBG_measured'
        ]
        return {
            'model': tf.keras.models.load_model('thyroid_dp_model.keras'),
            'scaler': pickle.load(open('scaler_thyroid.pkl', 'rb')),
            'features': features
        }
    except Exception:
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
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ===== REMOVE SIDEBAR COMPLETELY ===== */
    section[data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
    }
    
    /* ===== TOP-RIGHT FLOATING BUTTONS ===== */
    .st-key-top_settings_btn,
    .st-key-top_chat_btn,
    .st-key-top_email_btn,
    .st-key-top_web_btn {
        position: fixed !important;
        z-index: 999999 !important;
    }
    
    .st-key-top_settings_btn { top: 20px !important; right: 20px !important; }
    .st-key-top_chat_btn { top: 20px !important; right: 85px !important; }
    .st-key-top_email_btn { top: 20px !important; right: 150px !important; }
    .st-key-top_web_btn { top: 20px !important; right: 215px !important; }
    
    .st-key-top_settings_btn button,
    .st-key-top_chat_btn button,
    .st-key-top_email_btn button,
    .st-key-top_web_btn button {
        width: 52px !important;
        height: 52px !important;
        border-radius: 50% !important;
        color: white !important;
        font-size: 22px !important;
        border: 2px solid rgba(255, 255, 255, 0.25) !important;
        transition: all 0.3s ease !important;
        padding: 0 !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-width: 0 !important;
    }
    
    .st-key-top_settings_btn button:hover,
    .st-key-top_chat_btn button:hover,
    .st-key-top_email_btn button:hover,
    .st-key-top_web_btn button:hover {
        transform: scale(1.15) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.8) !important;
    }
    
    .st-key-top_settings_btn button { background: linear-gradient(135deg, #f59e0b, #d97706) !important; box-shadow: 0 4px 14px rgba(245, 158, 11, 0.5) !important; }
    .st-key-top_chat_btn button { background: linear-gradient(135deg, #10b981, #059669) !important; box-shadow: 0 4px 14px rgba(16, 185, 129, 0.5) !important; }
    .st-key-top_email_btn button { background: linear-gradient(135deg, #3b82f6, #2563eb) !important; box-shadow: 0 4px 14px rgba(59, 130, 246, 0.5) !important; }
    .st-key-top_web_btn button { background: linear-gradient(135deg, #8b5cf6, #7c3aed) !important; box-shadow: 0 4px 14px rgba(139, 92, 246, 0.5) !important; }
    
    /* ===== MAIN AREA ===== */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    .hero-header {
        background: linear-gradient(135deg, #667eea, #764ba2);
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
        background: radial-gradient(circle, rgba(255,255,255,0.1), transparent);
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
        background: linear-gradient(135deg, #1e1e2e, #2a2a3e);
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
        background: linear-gradient(135deg, #667eea, #764ba2);
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
        background: linear-gradient(135deg, #1a1a2e, #16213e);
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
    
    .feature-title { font-size: 1.1rem; font-weight: 600; color: #ffffff; margin-bottom: 6px; }
    .feature-desc { font-size: 0.9rem; color: #b0b0c0; line-height: 1.5; }
    
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
    
    .contact-card {
        background: linear-gradient(135deg, #1e1e2e, #2a2a3e);
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
    
    .contact-card .contact-icon { font-size: 1.8rem; margin-bottom: 8px; }
    .contact-card .contact-title { color: #ffffff; font-weight: 600; font-size: 1rem; margin-bottom: 5px; }
    .contact-card .contact-info { color: #b0b0c0; font-size: 0.88rem; line-height: 1.6; }
    .contact-card .contact-info strong { color: #10b981; font-size: 1rem; }
    
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
        background: linear-gradient(135deg, #1e1e2e, #2a2a3e);
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
    
    .gallery-image { width: 100%; height: 200px; object-fit: cover; display: block; }
    .gallery-body { padding: 18px 20px 22px 20px; }
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
    .gallery-title { font-size: 1.15rem; font-weight: 700; color: #ffffff; margin-bottom: 8px; }
    .gallery-desc { font-size: 0.88rem; color: #b0b0c0; line-height: 1.5; }
    
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
        padding: 0 18px !important;
        border-radius: 10px !important;
        background: transparent !important;
        color: #b0b0c0 !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        border: none !important;
        transition: all 0.25s ease !important;
        outline: none !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.12) !important;
        color: #ffffff !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(102, 126, 234, 0.35) !important;
        font-weight: 600 !important;
    }
    
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {
        background: transparent !important;
        display: none !important;
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
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        border: none !important;
        color: white !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3) !important;
    }
    
    .result-box {
        padding: 20px;
        border-radius: 12px;
        margin-top: 15px;
        border-left: 5px solid;
    }
    
    .result-high { background: rgba(239, 68, 68, 0.1); border-left-color: #ef4444; }
    .result-low { background: rgba(16, 185, 129, 0.1); border-left-color: #10b981; }
    .result-title { font-size: 1.2rem; font-weight: 700; margin-bottom: 8px; }
    .result-prob { font-size: 2rem; font-weight: 800; margin: 8px 0; }
    .result-desc { font-size: 0.9rem; color: #b0b0c0; }

    /* ===== CUSTOM LOADING SPINNER ===== */
    [data-testid="stStatusWidget"] {
        position: fixed !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        z-index: 9999999 !important;
        background: rgba(30, 30, 46, 0.95) !important;
        padding: 25px 45px !important;
        border-radius: 16px !important;
        border: 2px solid #667eea !important;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.5) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        min-width: 220px !important;
    }

    [data-testid="stStatusWidget"] > div {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 15px !important;
    }

    [data-testid="stStatusWidget"] span {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        letter-spacing: 0.5px !important;
    }

    [data-testid="stStatusWidget"] svg {
        width: 50px !important;
        height: 50px !important;
    }
</style>
""", unsafe_allow_html=True)


ui.inject_ui_css()


# ========================================
# TOP-RIGHT FLOATING BUTTONS
# ========================================
current_user = st.session_state.user
is_patient = current_user.get('role') == 'patient'
role_label = "Patient" if is_patient else "Doctor"
user_email = current_user.get('email', 'guest@medifederate')

avatar_emoji = "👤" if is_patient else "👨‍⚕️"

if st.button(avatar_emoji, key="top_settings_btn", help="Settings & Account"):
    show_settings_dialog()

if st.button("💬", key="top_chat_btn", help="Open MediBot Chat"):
    st.session_state.show_chat_page = True
    st.rerun()

if st.button("📧", key="top_email_btn", help="Email Support"):
    st.session_state.show_email_page = True
    st.rerun()

if st.button("🌐", key="top_web_btn", help="Visit Website"):
    st.session_state.show_website_page = True
    st.rerun()


# ========================================
# HERO HEADER
# ========================================
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
# MAIN TABS
# ========================================
if is_patient:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📈 Overview", "🩸 Diabetes", "❤️ Heart Disease", "🧠 Stroke",
        "🫘 Kidney", "🧬 Thyroid", "🏥 Gallery", "📞 Contacts"
    ])
    tab9 = None
else:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "📈 Overview", "🩸 Diabetes", "❤️ Heart Disease", "🧠 Stroke",
        "🫘 Kidney", "🧬 Thyroid", "🏥 Gallery", "📞 Contacts", "📜 History"
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
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        ui.animated_metric_card("🩸", "Diabetes", "62.38%", "100,244 patients", "Beats Baseline", "success")
    
    with col2:
        ui.animated_metric_card("❤️", "Heart Disease", "88.52%", "303 patients", "⭐ Best", "warning")
    
    with col3:
        ui.animated_metric_card("🧠", "Stroke", "72.90%", "5,109 patients", "80% Recall", "info")
    
    with col4:
        ui.animated_metric_card("🫘", "Kidney", "100%", "400 patients", "🎯 Excellent", "success")

    with col5:
        ui.animated_metric_card("🧬", "Thyroid", "54.67%", "3,000 patients", "Baseline", "info")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">📊 Model Comparison</div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        comparison = pd.DataFrame({
            "Disease": ["Diabetes", "Heart Disease", "Stroke", "Kidney Disease", "Thyroid"],
            "Accuracy (%)": [62.38, 88.52, 72.90, 100.00, 54.67],
            "Data Shared": ["0 B", "0 B", "0 B", "0 B", "0 B"],
            "Privacy": ["✅ DP", "✅ DP", "✅ DP", "✅ DP", "✅ DP"]
        })
        st.dataframe(comparison, width='stretch', hide_index=True)
    
    with col_b:
        fig = ui.plotly_model_comparison(comparison)
        st.plotly_chart(fig, width='stretch', config={'displayModeBar': False}, key="overview_chart")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">✨ Key Features</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card fade-in">
            <div class="feature-title">🔒 Privacy-Preserving</div>
            <div class="feature-desc">Patient data never leaves the hospital. Only encrypted model weights are shared.</div>
        </div>
        <div class="feature-card fade-in">
            <div class="feature-title">🌐 Federated Learning</div>
            <div class="feature-desc">3 simulated hospitals collaboratively train a shared model without centralizing data.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card fade-in">
            <div class="feature-title">🧠 Explainable AI</div>
            <div class="feature-desc">SHAP-based analysis shows why each prediction was made — critical for medical trust.</div>
        </div>
        <div class="feature-card fade-in">
            <div class="feature-title">💬 AI Health Chatbot</div>
            <div class="feature-desc">MediBot answers health questions with an intelligent, easy-to-use interface.</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.success("✅ **5 diseases** predicted using real trained neural networks with Federated Learning + Differential Privacy — **ZERO patient data shared!**")


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
        loading_placeholder = st.empty()
        with loading_placeholder.container():
            ui.prediction_loading_animation("Diabetes")
        
        model = load_diabetes_model()
        
        data = {
            'age': age, 'time_in_hospital': time_hosp,
            'num_medications': meds, 'num_lab_procedures': lab,
            'number_diagnoses': diag, 'num_procedures': proc,
            'number_inpatient': inpat, 'number_emergency': emerg,
        }
        
        prob = predict_with_model(model, data)
        loading_placeholder.empty()
        
        if prob is not None:
            st.info(f"**Patient Summary:** Age {age} · {time_hosp} days in hospital · {meds} medications")
            pct = prob * 100
            
            ui.result_card_with_animation(
                prob > 0.5,
                "High Risk of Readmission" if prob > 0.5 else "Low Risk of Readmission",
                pct,
                "This patient has a high probability of being readmitted. Close monitoring is recommended." if prob > 0.5 else "This patient has a low probability of readmission. Standard follow-up is sufficient."
            )
            
            hist.save_prediction(
                "Diabetes", prob,
                "High Risk" if prob > 0.5 else "Low Risk",
                f"Age: {age}, Time: {time_hosp}d, Meds: {meds}, Lab: {lab}, Diag: {diag}",
                user_email=user_email
            )
            
            pdf_bytes = generate_medical_report(
                "Diabetes",
                {"Age": age, "Time in Hospital (days)": time_hosp, "Number of Medications": meds,
                 "Lab Procedures": lab, "Number of Diagnoses": diag, "Procedures": proc,
                 "Previous Inpatient Visits": inpat, "Previous Emergency Visits": emerg},
                {"probability": prob, "is_high_risk": prob > 0.5,
                 "summary": f"Patient has {pct:.1f}% probability of readmission."}
            )
            st.download_button(
                label="📄  Download PDF Report", data=pdf_bytes,
                file_name=f"MediFederate_Diabetes_Report_{age}y_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf", width='stretch', key="d_download_btn"
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
        loading_placeholder = st.empty()
        with loading_placeholder.container():
            ui.prediction_loading_animation("Heart Disease")
        
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
        loading_placeholder.empty()
        
        if prob is not None:
            st.info(f"**Patient Summary:** Age {age_h} · {sex_h} · BP {trestbps} · Chol {chol}")
            pct = prob * 100
            
            ui.result_card_with_animation(
                prob > 0.5,
                "High Risk of Heart Disease" if prob > 0.5 else "Low Risk of Heart Disease",
                pct,
                "This patient shows signs of heart disease. Further cardiac evaluation is recommended." if prob > 0.5 else "This patient shows low risk for heart disease. Routine checkup is sufficient."
            )
            
            hist.save_prediction(
                "Heart Disease", prob,
                "High Risk" if prob > 0.5 else "Low Risk",
                f"Age: {age_h}, {sex_h}, BP: {trestbps}, Chol: {chol}, MaxHR: {thalach}",
                user_email=user_email
            )
            
            pdf_bytes = generate_medical_report(
                "Heart Disease",
                {"Age": age_h, "Gender": sex_h, "Chest Pain Type": cp_h,
                 "Resting BP (mm Hg)": trestbps, "Cholesterol (mg/dl)": chol,
                 "Fasting Blood Sugar > 120": fbs, "Resting ECG": restecg,
                 "Max Heart Rate": thalach, "Exercise Induced Angina": exang,
                 "ST Depression": oldpeak, "Slope": slope,
                 "Major Vessels": ca, "Thalassemia": thal},
                {"probability": prob, "is_high_risk": prob > 0.5,
                 "summary": f"Patient has {pct:.1f}% probability of heart disease."}
            )
            st.download_button(
                label="📄  Download PDF Report", data=pdf_bytes,
                file_name=f"MediFederate_Heart_Report_{age_h}y_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf", width='stretch', key="h_download_btn"
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
        loading_placeholder = st.empty()
        with loading_placeholder.container():
            ui.prediction_loading_animation("Stroke")
        
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
        loading_placeholder.empty()
        
        if prob is not None:
            st.info(f"**Patient Summary:** Age {age_s} · {gender_s} · Glucose {glucose} · BMI {bmi}")
            pct = prob * 100
            
            ui.result_card_with_animation(
                prob > 0.5,
                "High Risk of Stroke" if prob > 0.5 else "Low Risk of Stroke",
                pct,
                "This patient has a high risk of stroke. Immediate medical consultation is recommended." if prob > 0.5 else "This patient has a low risk of stroke. Maintain a healthy lifestyle."
            )
            
            hist.save_prediction(
                "Stroke", prob,
                "High Risk" if prob > 0.5 else "Low Risk",
                f"Age: {age_s}, {gender_s}, Glucose: {glucose}, BMI: {bmi}, Smoking: {smoking}",
                user_email=user_email
            )
            
            pdf_bytes = generate_medical_report(
                "Stroke",
                {"Age": age_s, "Gender": gender_s, "Hypertension": hyp,
                 "Heart Disease": heart, "Ever Married": married,
                 "Average Glucose Level": glucose, "BMI": bmi,
                 "Work Type": work, "Residence": residence, "Smoking Status": smoking},
                {"probability": prob, "is_high_risk": prob > 0.5,
                 "summary": f"Patient has {pct:.1f}% probability of stroke."}
            )
            st.download_button(
                label="📄  Download PDF Report", data=pdf_bytes,
                file_name=f"MediFederate_Stroke_Report_{age_s}y_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf", width='stretch', key="s_download_btn"
            )
        else:
            st.error("⚠️ Stroke model not loaded.")


# ========================================
# TAB 5: KIDNEY DISEASE
# ========================================
with tab5:
    st.markdown('<div class="section-header">🫘 Kidney Disease Prediction</div>', unsafe_allow_html=True)
    
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("Accuracy", "100%", "🎯 Excellent")
    with col_info2:
        st.metric("Training Data", "400 patients")
    with col_info3:
        st.metric("Privacy", "✅ DP Enabled")
    
    st.markdown("---")
    st.markdown("#### Enter Patient Details")
    
    col1, col2 = st.columns(2)
    with col1:
        age_k = st.slider("Age", 1, 100, 50, key="k_age")
        bp_k = st.slider("Blood Pressure (mm Hg)", 50, 180, 80, key="k_bp")
        sg_k = st.slider("Specific Gravity", 1.005, 1.025, 1.020, step=0.005, key="k_sg")
        al_k = st.slider("Albumin (0-5)", 0, 5, 1, key="k_al")
        su_k = st.slider("Sugar (0-5)", 0, 5, 0, key="k_su")
        bgr_k = st.slider("Blood Glucose Random", 50, 500, 120, key="k_bgr")
        bu_k = st.slider("Blood Urea", 10, 400, 40, key="k_bu")
        sc_k = st.slider("Serum Creatinine", 0.5, 20.0, 1.2, step=0.1, key="k_sc")
        sod_k = st.slider("Sodium", 100, 170, 140, key="k_sod")
        pot_k = st.slider("Potassium", 2.0, 50.0, 4.5, step=0.1, key="k_pot")
    with col2:
        hemo_k = st.slider("Hemoglobin", 3.0, 20.0, 14.0, step=0.1, key="k_hemo")
        pcv_k = st.slider("Packed Cell Volume", 10, 60, 40, key="k_pcv")
        wc_k = st.slider("White Blood Cell Count", 2000, 25000, 8000, key="k_wc")
        rc_k = st.slider("Red Blood Cell Count", 2.0, 8.0, 5.0, step=0.1, key="k_rc")
        htn_k = st.selectbox("Hypertension", ["No", "Yes"], key="k_htn")
        dm_k = st.selectbox("Diabetes Mellitus", ["No", "Yes"], key="k_dm")
        cad_k = st.selectbox("Coronary Artery Disease", ["No", "Yes"], key="k_cad")
        appet_k = st.selectbox("Appetite", ["Good", "Poor"], key="k_appet")
        pe_k = st.selectbox("Pedal Edema", ["No", "Yes"], key="k_pe")
        ane_k = st.selectbox("Anemia", ["No", "Yes"], key="k_ane")
    
    if st.button("🔮 Predict Kidney Disease", type="primary", key="k_btn"):
        loading_placeholder = st.empty()
        with loading_placeholder.container():
            ui.prediction_loading_animation("Kidney Disease")
        
        model = load_kidney_model()
        
        data = {
            'age': float(age_k), 'bp': float(bp_k), 'sg': float(sg_k),
            'al': float(al_k), 'su': float(su_k), 'bgr': float(bgr_k),
            'bu': float(bu_k), 'sc': float(sc_k), 'sod': float(sod_k),
            'pot': float(pot_k), 'hemo': float(hemo_k), 'pcv': float(pcv_k),
            'wc': float(wc_k), 'rc': float(rc_k),
            'htn': 1.0 if htn_k == "Yes" else 0.0,
            'dm': 1.0 if dm_k == "Yes" else 0.0,
            'cad': 1.0 if cad_k == "Yes" else 0.0,
            'appet': 1.0 if appet_k == "Good" else 0.0,
            'pe': 1.0 if pe_k == "Yes" else 0.0,
            'ane': 1.0 if ane_k == "Yes" else 0.0,
            'rbc': 1.0, 'pc': 1.0, 'pcc': 0.0, 'ba': 0.0,
        }
        
        prob = predict_with_model(model, data)
        loading_placeholder.empty()
        
        if prob is not None:
            st.info(f"**Patient Summary:** Age {age_k} · BP {bp_k} · Hemoglobin {hemo_k} · Creatinine {sc_k}")
            pct = prob * 100
            
            ui.result_card_with_animation(
                prob > 0.5,
                "High Risk of Kidney Disease" if prob > 0.5 else "Low Risk of Kidney Disease",
                pct,
                "This patient shows signs of kidney disease. Immediate nephrology consultation is recommended." if prob > 0.5 else "This patient shows low risk for kidney disease. Routine checkup is sufficient."
            )
            
            hist.save_prediction(
                "Kidney Disease", prob,
                "High Risk" if prob > 0.5 else "Low Risk",
                f"Age: {age_k}, BP: {bp_k}, Hemoglobin: {hemo_k}, Creatinine: {sc_k}",
                user_email=user_email
            )
            
            pdf_bytes = generate_medical_report(
                "Kidney Disease",
                {"Age": age_k, "Blood Pressure": bp_k, "Hemoglobin": hemo_k,
                 "Serum Creatinine": sc_k, "Blood Urea": bu_k,
                 "Sodium": sod_k, "Potassium": pot_k,
                 "Hypertension": htn_k, "Diabetes": dm_k, "Anemia": ane_k},
                {"probability": prob, "is_high_risk": prob > 0.5,
                 "summary": f"Patient has {pct:.1f}% probability of kidney disease."}
            )
            st.download_button(
                label="📄  Download PDF Report", data=pdf_bytes,
                file_name=f"MediFederate_Kidney_Report_{age_k}y_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf", width='stretch', key="k_download_btn"
            )
        else:
            st.error("⚠️ Kidney model not loaded.")


# ========================================
# TAB 6: THYROID DISEASE
# ========================================
with tab6:
    st.markdown('<div class="section-header">🧬 Thyroid Disease Prediction</div>', unsafe_allow_html=True)
    
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("Accuracy", "54.67%", "Baseline (Synthetic)")
    with col_info2:
        st.metric("Training Data", "3,000 patients")
    with col_info3:
        st.metric("Privacy", "✅ DP Enabled")
    
    st.markdown("---")
    st.markdown("#### Enter Patient Details")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        t_age = st.number_input("Age", 1, 100, 45, key="t_age")
        t_sex = st.selectbox("Gender", ["Female", "Male"], key="t_sex")
        t_tsh = st.number_input("TSH Level", 0.0, 50.0, 2.0, step=0.1, key="t_tsh")
        t_t3 = st.number_input("T3 Level", 0.0, 10.0, 1.5, step=0.1, key="t_t3")
        t_tt4 = st.number_input("TT4 Level", 0.0, 30.0, 8.0, step=0.1, key="t_tt4")
        t_t4u = st.number_input("T4U Level", 0.0, 3.0, 1.0, step=0.1, key="t_t4u")
        t_fti = st.number_input("FTI Level", 0.0, 30.0, 8.0, step=0.1, key="t_fti")
        t_on_thy = st.selectbox("On Thyroxine", ["No", "Yes"], key="t_on_thy")
        t_query_thy = st.selectbox("Query on Thyroxine", ["No", "Yes"], key="t_query_thy")
        t_anti_thy = st.selectbox("On Antithyroid Meds", ["No", "Yes"], key="t_anti_thy")
    with col2:
        t_sick = st.selectbox("Sick", ["No", "Yes"], key="t_sick")
        t_pregnant = st.selectbox("Pregnant", ["No", "Yes"], key="t_pregnant")
        t_surgery = st.selectbox("Thyroid Surgery", ["No", "Yes"], key="t_surgery")
        t_i131 = st.selectbox("I131 Treatment", ["No", "Yes"], key="t_i131")
        t_query_hypo = st.selectbox("Query Hypothyroid", ["No", "Yes"], key="t_query_hypo")
        t_query_hyper = st.selectbox("Query Hyperthyroid", ["No", "Yes"], key="t_query_hyper")
        t_lithium = st.selectbox("Lithium", ["No", "Yes"], key="t_lithium")
        t_goitre = st.selectbox("Goitre", ["No", "Yes"], key="t_goitre")
        t_tumor = st.selectbox("Tumor", ["No", "Yes"], key="t_tumor")
    with col3:
        t_hypopit = st.selectbox("Hypopituitary", ["No", "Yes"], key="t_hypopit")
        t_psych = st.selectbox("Psych", ["No", "Yes"], key="t_psych")
        t_tsh_meas = st.selectbox("TSH Measured", ["No", "Yes"], key="t_tsh_meas")
        t_t3_meas = st.selectbox("T3 Measured", ["No", "Yes"], key="t_t3_meas")
        t_tt4_meas = st.selectbox("TT4 Measured", ["No", "Yes"], key="t_tt4_meas")
        t_t4u_meas = st.selectbox("T4U Measured", ["No", "Yes"], key="t_t4u_meas")
        t_fti_meas = st.selectbox("FTI Measured", ["No", "Yes"], key="t_fti_meas")
        t_tbg_meas = st.selectbox("TBG Measured", ["No", "Yes"], key="t_tbg_meas")
    
    if st.button("🔮 Predict Thyroid Risk", type="primary", key="t_btn"):
        loading_placeholder = st.empty()
        with loading_placeholder.container():
            ui.prediction_loading_animation("Thyroid")
        
        model = load_thyroid_model()
        
        data = {
            'age': float(t_age), 'sex': 1.0 if t_sex == "Male" else 0.0,
            'TSH': float(t_tsh), 'T3': float(t_t3), 'TT4': float(t_tt4),
            'T4U': float(t_t4u), 'FTI': float(t_fti),
            'on_thyroxine': 1.0 if t_on_thy == "Yes" else 0.0,
            'query_on_thyroxine': 1.0 if t_query_thy == "Yes" else 0.0,
            'on_antithyroid_meds': 1.0 if t_anti_thy == "Yes" else 0.0,
            'sick': 1.0 if t_sick == "Yes" else 0.0,
            'pregnant': 1.0 if t_pregnant == "Yes" else 0.0,
            'thyroid_surgery': 1.0 if t_surgery == "Yes" else 0.0,
            'I131_treatment': 1.0 if t_i131 == "Yes" else 0.0,
            'query_hypothyroid': 1.0 if t_query_hypo == "Yes" else 0.0,
            'query_hyperthyroid': 1.0 if t_query_hyper == "Yes" else 0.0,
            'lithium': 1.0 if t_lithium == "Yes" else 0.0,
            'goitre': 1.0 if t_goitre == "Yes" else 0.0,
            'tumor': 1.0 if t_tumor == "Yes" else 0.0,
            'hypopituitary': 1.0 if t_hypopit == "Yes" else 0.0,
            'psych': 1.0 if t_psych == "Yes" else 0.0,
            'TSH_measured': 1.0 if t_tsh_meas == "Yes" else 0.0,
            'T3_measured': 1.0 if t_t3_meas == "Yes" else 0.0,
            'TT4_measured': 1.0 if t_tt4_meas == "Yes" else 0.0,
            'T4U_measured': 1.0 if t_t4u_meas == "Yes" else 0.0,
            'FTI_measured': 1.0 if t_fti_meas == "Yes" else 0.0,
            'TBG_measured': 1.0 if t_tbg_meas == "Yes" else 0.0
        }
        
        prob = predict_with_model(model, data)
        loading_placeholder.empty()
        
        if prob is not None:
            st.info(f"**Patient Summary:** Age {t_age} · {t_sex} · TSH {t_tsh} · T3 {t_t3} · TT4 {t_tt4}")
            pct = prob * 100
            
            ui.result_card_with_animation(
                prob > 0.5,
                "High Risk of Thyroid Disease" if prob > 0.5 else "Low Risk of Thyroid Disease",
                pct,
                "This patient has a high probability of thyroid disease. Endocrinology consultation is recommended." if prob > 0.5 else "This patient has a low probability of thyroid disease. Routine follow-up is sufficient."
            )
            
            hist.save_prediction(
                "Thyroid", prob,
                "High Risk" if prob > 0.5 else "Low Risk",
                f"Age: {t_age}, TSH: {t_tsh}, T3: {t_t3}, TT4: {t_tt4}",
                user_email=user_email
            )
            
            pdf_bytes = generate_medical_report(
                "Thyroid Disease",
                {"Age": t_age, "Gender": t_sex, "TSH": t_tsh, "T3": t_t3, "TT4": t_tt4, "T4U": t_t4u, "FTI": t_fti},
                {"probability": prob, "is_high_risk": prob > 0.5,
                 "summary": f"Patient has {pct:.1f}% probability of thyroid disease."}
            )
            st.download_button(
                label="📄  Download PDF Report", data=pdf_bytes,
                file_name=f"MediFederate_Thyroid_Report_{t_age}y_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf", width='stretch', key="t_download_btn"
            )
        else:
            st.error("⚠️ Thyroid model not loaded.")


# ========================================
# TAB 7: GALLERY
# ========================================
with tab7:
    st.markdown('<div class="section-header">🏥 Medical Knowledge Gallery</div>', unsafe_allow_html=True)
    st.markdown("Explore important health conditions, their symptoms, and prevention tips.")
    
    gallery_items = [
        {"category": "CARDIOLOGY", "title": "Blood Pressure Monitoring", "desc": "High BP is a silent killer. Get checked regularly — normal is 120/80 mm Hg.", "image": "https://images.unsplash.com/photo-1579154204601-01588f351e67?w=800&auto=format&fit=crop", "emoji": "💓", "query": "My blood pressure is high, what should I do?"},
        {"category": "CARDIOLOGY", "title": "Heart Health", "desc": "Cardiovascular disease is the #1 cause of death globally.", "image": "https://images.unsplash.com/photo-1628348070889-cb656235b4eb?w=800&auto=format&fit=crop", "emoji": "❤️", "query": "I have chest pain, what should I do?"},
        {"category": "ENDOCRINOLOGY", "title": "Diabetes & Blood Sugar", "desc": "Over 537M adults live with diabetes. Monitor sugar regularly.", "image": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=800&auto=format&fit=crop", "emoji": "🩸", "query": "My sugar level is 200, what should I do?"},
        {"category": "NEPHROLOGY", "title": "Kidney Health", "desc": "Kidneys filter your blood. Stay hydrated and control BP.", "image": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=800&auto=format&fit=crop", "emoji": "🫘", "query": "How can I keep my kidneys healthy?"},
        {"category": "NEUROLOGY", "title": "Stroke Awareness", "desc": "Remember FAST: Face, Arm, Speech, Time. Every minute counts!", "image": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&auto=format&fit=crop", "emoji": "🧠", "query": "Tell me about stroke symptoms"},
        {"category": "ENDOCRINOLOGY", "title": "Thyroid Health", "desc": "Thyroid disorders affect metabolism. Get TSH, T3, T4 checked if symptomatic.", "image": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=800&auto=format&fit=crop", "emoji": "🧬", "query": "What are the symptoms of thyroid problems?"},
        {"category": "GENERAL HEALTH", "title": "Fever & Infections", "desc": "Fever is the body's defense against infection.", "image": "https://images.unsplash.com/photo-1584362917165-526a968579e8?w=800&auto=format&fit=crop", "emoji": "🌡️", "query": "I have fever, what should I do?"},
        {"category": "GASTROENTEROLOGY", "title": "Stomach & Digestion", "desc": "Avoid spicy, oily food. Eat smaller meals.", "image": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=800&auto=format&fit=crop", "emoji": "🤢", "query": "I have stomach pain, what should I do?"},
        {"category": "HEMATOLOGY", "title": "Blood Health", "desc": "Regular blood tests help detect conditions early.", "image": "https://images.unsplash.com/photo-1631815589968-fdb09a223b1e?w=800&auto=format&fit=crop", "emoji": "🩸", "query": "I am feeling weakness, what should I do?"},
        {"category": "PHARMACOLOGY", "title": "Medication Safety", "desc": "Never self-medicate. Take antibiotics only when prescribed.", "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800&auto=format&fit=crop", "emoji": "💊", "query": "How should I take my medicines?"},
        {"category": "PREVENTIVE CARE", "title": "Regular Checkups", "desc": "Annual health checkups catch problems early.", "image": "https://images.unsplash.com/photo-1584982751601-97dcc096659c?w=800&auto=format&fit=crop", "emoji": "🩺", "query": "How often should I get a health checkup?"},
        {"category": "EMERGENCY", "title": "Emergency Response", "desc": "Save these numbers: Rescue 1122, Edhi 115, Police 15, Chhipa 1020.", "image": "https://images.unsplash.com/photo-1587745416684-47953f16f02f?w=800&auto=format&fit=crop", "emoji": "🚨", "query": "What is the emergency number in Pakistan?"},
    ]
    
    for i in range(0, len(gallery_items), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            item = gallery_items[i]
            st.markdown(f"""
            <div class="gallery-card fade-in">
                <img src="{item['image']}" class="gallery-image" onerror="this.style.display='none'"/>
                <div class="gallery-body">
                    <span class="gallery-category">{item['category']}</span>
                    <div class="gallery-title">{item['emoji']} {item['title']}</div>
                    <div class="gallery-desc">{item['desc']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"💬 Ask MediBot about {item['title']}", key=f"gal_btn_{i}", width='stretch'):
                st.session_state.show_chat_page = True
                st.session_state.pending_chat_query = item['query']
                st.rerun()
        
        with col2:
            if i + 1 < len(gallery_items):
                item = gallery_items[i + 1]
                st.markdown(f"""
                <div class="gallery-card fade-in">
                    <img src="{item['image']}" class="gallery-image" onerror="this.style.display='none'"/>
                    <div class="gallery-body">
                        <span class="gallery-category">{item['category']}</span>
                        <div class="gallery-title">{item['emoji']} {item['title']}</div>
                        <div class="gallery-desc">{item['desc']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"💬 Ask MediBot about {item['title']}", key=f"gal_btn_{i+1}", width='stretch'):
                    st.session_state.show_chat_page = True
                    st.session_state.pending_chat_query = item['query']
                    st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 **Tip:** Click the 'Ask MediBot' button under any card, and the AI will instantly answer questions about that topic!")


# ========================================
# TAB 8: CONTACTS
# ========================================
with tab8:
    st.markdown('<div class="section-header">📞 Contacts & Helpline</div>', unsafe_allow_html=True)
    
    st.markdown("##### 🚨 Emergency Numbers")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="contact-card fade-in">
            <div class="emergency-badge">Emergency</div>
            <div class="contact-icon">🚨</div>
            <div class="contact-title">Rescue</div>
            <div class="contact-info"><strong>1122</strong></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="contact-card fade-in">
            <div class="emergency-badge">Ambulance</div>
            <div class="contact-icon">🚑</div>
            <div class="contact-title">Edhi Ambulance</div>
            <div class="contact-info"><strong>115</strong></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="contact-card fade-in">
            <div class="emergency-badge">Police</div>
            <div class="contact-icon">👮</div>
            <div class="contact-title">Police</div>
            <div class="contact-info"><strong>15</strong></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="contact-card fade-in">
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
            <div class="contact-info">📍 Karachi<br>📞 +92-21-111-911-911<br>🌐 hospitals.aku.edu</div>
        </div>
        <div class="contact-card">
            <div class="contact-icon">🏥</div>
            <div class="contact-title">Mayo Hospital</div>
            <div class="contact-info">📍 Lahore<br>📞 +92-42-99211112<br>🌐 mayo-hospital.gov.pk</div>
        </div>
        <div class="contact-card">
            <div class="contact-icon">🏥</div>
            <div class="contact-title">PIMS Islamabad</div>
            <div class="contact-info">📍 Islamabad<br>📞 +92-51-9261170<br>🌐 pims.gov.pk</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="contact-card">
            <div class="contact-icon">🏥</div>
            <div class="contact-title">Shaukat Khanum Memorial Hospital</div>
            <div class="contact-info">📍 Lahore & Peshawar<br>📞 +92-42-35905000<br>🌐 shaukatkhanum.org.pk</div>
        </div>
        <div class="contact-card">
            <div class="contact-icon">🏥</div>
            <div class="contact-title">Jinnah Postgraduate Medical Centre</div>
            <div class="contact-info">📍 Karachi<br>📞 +92-21-99201300<br>🌐 jpmc.edu.pk</div>
        </div>
        <div class="contact-card">
            <div class="contact-icon">🏥</div>
            <div class="contact-title">Services Hospital Lahore</div>
            <div class="contact-info">📍 Lahore<br>📞 +92-42-99203402<br>🌐 serviceshospital.punjab.gov.pk</div>
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
# TAB 9: HISTORY (Doctor Only)
# ========================================
if tab9 is not None:
    with tab9:
        st.markdown('<div class="section-header">📜 My Prediction History</div>', unsafe_allow_html=True)
        st.markdown(f"""
        Showing predictions for: **{current_user['full_name']}** ({current_user['email']})
        
        *These are your own predictions. Other doctors' history is private and not visible to you.*
        """)
        
        stats = hist.get_statistics(user_email=user_email)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            ui.animated_metric_card("📊", "My Predictions", str(stats['total']))
        
        with col2:
            ui.animated_metric_card("🔴", "High Risk", str(stats['high_risk']))
        
        with col3:
            ui.animated_metric_card("🟢", "Low Risk", str(stats['low_risk']))
        
        with col4:
            ui.animated_metric_card("🏥", "Diseases", "5")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_f1, col_f2, col_f3 = st.columns([2, 2, 1])
        
        with col_f1:
            disease_filter = st.selectbox(
                "🔍 Filter by Disease",
                ["All", "Diabetes", "Heart Disease", "Stroke", "Kidney Disease", "Thyroid"],
                key="hist_filter"
            )
        
        with col_f2:
            st.markdown("&nbsp;")
            csv_data = hist.export_to_csv(user_email=user_email)
            st.download_button(
                label="📥  Export My History to CSV", data=csv_data,
                file_name=f"My_Predictions_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv", width='stretch', key="hist_export"
            )
        
        with col_f3:
            st.markdown("&nbsp;")
            if st.button("🗑️  Clear My History", width='stretch', key="hist_clear"):
                hist.clear_all_predictions(user_email=user_email)
                st.success("Your history cleared!")
                st.rerun()
        
        st.markdown("---")
        st.markdown("##### 📊 My Analytics")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            disease_dist = hist.get_disease_distribution(user_email=user_email)
            fig1 = ui.plotly_disease_donut(disease_dist, "My Disease Distribution")
            st.plotly_chart(fig1, width='stretch', config={'displayModeBar': False}, key="hist_disease_chart")
        
        with col_chart2:
            risk_dist = hist.get_risk_distribution(user_email=user_email)
            fig2 = ui.plotly_risk_bars(risk_dist, "My Risk Distribution")
            st.plotly_chart(fig2, width='stretch', config={'displayModeBar': False}, key="hist_risk_chart")
        
        st.markdown("---")
        st.markdown("##### 📋 My Predictions")
        
        df = hist.get_all_predictions(disease_filter=disease_filter, user_email=user_email)
        
        if not df.empty:
            cols_to_show = ['id', 'timestamp', 'disease', 'probability', 'risk_level']
            display_df = df[cols_to_show].copy()
            display_df['probability'] = (display_df['probability'] * 100).round(1).astype(str) + '%'
            
            st.dataframe(display_df, width='stretch', hide_index=True)
            
            st.markdown("---")
            st.markdown("##### 🔍 View Details")
            
            selected_id = st.selectbox(
                "Select Prediction ID to view details:",
                df['id'].tolist(), key="hist_detail"
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
            st.info("📭 You have not made any predictions yet. Go to Diabetes, Heart, Stroke, Kidney, or Thyroid tab to make your first prediction!")


# ========================================
# LEGAL LINKS FOOTER
# ========================================
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

col_l1, col_l2, col_l3 = st.columns(3)

with col_l1:
    if st.button("📋  Privacy Policy", width='stretch', key="footer_privacy"):
        st.session_state.show_privacy_page = True
        st.rerun()

with col_l2:
    if st.button("📜  Terms of Service", width='stretch', key="footer_terms"):
        st.session_state.show_terms_page = True
        st.rerun()

with col_l3:
    if st.button("📧  Contact Support", width='stretch', key="footer_contact"):
        st.session_state.show_email_page = True
        st.rerun()


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