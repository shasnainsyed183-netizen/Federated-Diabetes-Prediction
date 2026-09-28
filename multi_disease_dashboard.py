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
# INFO & LEGAL PAGES SWITCHING
# ========================================
for key in ['show_email_page', 'show_website_page', 'show_privacy_page', 'show_terms_page']:
    if key not in st.session_state:
        st.session_state[key] = False

if st.session_state.show_email_page:
    render_email_page(); st.stop()
if st.session_state.show_website_page:
    render_website_page(); st.stop()
if st.session_state.show_privacy_page:
    render_privacy_policy(); st.stop()
if st.session_state.show_terms_page:
    render_terms_of_service(); st.stop()


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
        return {'model': tf.keras.models.load_model('federated_dp_model.keras'),
                'scaler': pickle.load(open('scaler.pkl', 'rb')),
                'features': pickle.load(open('feature_names.pkl', 'rb'))}
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def load_heart_model():
    import tensorflow as tf
    try:
        return {'model': tf.keras.models.load_model('heart_dp_model.keras'),
                'scaler': pickle.load(open('scaler_heart.pkl', 'rb')),
                'features': pickle.load(open('feature_names_heart.pkl', 'rb'))}
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def load_stroke_model():
    import tensorflow as tf
    try:
        return {'model': tf.keras.models.load_model('stroke_dp_model.keras'),
                'scaler': pickle.load(open('scaler_stroke.pkl', 'rb')),
                'features': pickle.load(open('feature_names_stroke.pkl', 'rb'))}
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def load_kidney_model():
    import tensorflow as tf
    try:
        return {'model': tf.keras.models.load_model('kidney_dp_model.keras'),
                'scaler': pickle.load(open('scaler_kidney.pkl', 'rb')),
                'features': pickle.load(open('feature_names_kidney.pkl', 'rb'))}
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def load_thyroid_model():
    import tensorflow as tf
    try:
        return {'model': tf.keras.models.load_model('thyroid_dp_model.keras'),
                'scaler': pickle.load(open('scaler_thyroid.pkl', 'rb')),
                'features': pickle.load(open('thyroid_features.pkl', 'rb'))}
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
# PATIENT INFORMATION HELPER
# ========================================
def render_patient_info(form_key):
    """Renders patient demographic info fields. Returns dict."""
    st.markdown("##### 👤 Patient Information")
    col1, col2 = st.columns(2)
    with col1:
        p_name = st.text_input("Patient Full Name", placeholder="Enter patient's full name", key=f"{form_key}_pname")
        p_father = st.text_input("Father / Husband Name", placeholder="Enter father or husband name", key=f"{form_key}_pfather")
        p_contact = st.text_input("Contact Number", placeholder="03XX-XXXXXXX", key=f"{form_key}_pcontact")
    with col2:
        p_age_input = st.text_input("Age (Years)", placeholder="e.g., 45", key=f"{form_key}_page")
        p_cnic = st.text_input("CNIC (Optional)", placeholder="XXXXX-XXXXXXX-X", key=f"{form_key}_pcnic")
        p_address = st.text_input("City / Address", placeholder="e.g., Lahore", key=f"{form_key}_paddress")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### 🩺 Clinical Details")
    
    return {
        "Patient Name": p_name if p_name else "N/A",
        "Father/Husband Name": p_father if p_father else "N/A",
        "Contact": p_contact if p_contact else "N/A",
        "CNIC": p_cnic if p_cnic else "N/A",
        "City": p_address if p_address else "N/A",
        "Date of Visit": datetime.now().strftime("%Y-%m-%d"),
    }


# ========================================
# CUSTOM CSS
# ========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    section[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"] { display: none !important; visibility: hidden !important; width: 0 !important; }
    
    .st-key-top_settings_btn, .st-key-top_chat_btn, .st-key-top_email_btn, .st-key-top_web_btn { position: fixed !important; z-index: 999999 !important; }
    .st-key-top_settings_btn { top: 20px !important; right: 20px !important; }
    .st-key-top_chat_btn { top: 20px !important; right: 85px !important; }
    .st-key-top_email_btn { top: 20px !important; right: 150px !important; }
    .st-key-top_web_btn { top: 20px !important; right: 215px !important; }
    
    .st-key-top_settings_btn button, .st-key-top_chat_btn button, .st-key-top_email_btn button, .st-key-top_web_btn button {
        width: 52px !important; height: 52px !important; border-radius: 50% !important; color: white !important;
        font-size: 22px !important; border: 2px solid rgba(255, 255, 255, 0.25) !important;
        transition: all 0.3s ease !important; padding: 0 !important; cursor: pointer !important;
        display: flex !important; align-items: center !important; justify-content: center !important; min-width: 0 !important;
    }
    .st-key-top_settings_btn button:hover, .st-key-top_chat_btn button:hover, .st-key-top_email_btn button:hover, .st-key-top_web_btn button:hover {
        transform: scale(1.15) !important; box-shadow: 0 6px 20px rgba(102, 126, 234, 0.8) !important;
    }
    .st-key-top_settings_btn button { background: linear-gradient(135deg, #f59e0b, #d97706) !important; }
    .st-key-top_chat_btn button { background: linear-gradient(135deg, #10b981, #059669) !important; }
    .st-key-top_email_btn button { background: linear-gradient(135deg, #3b82f6, #2563eb) !important; }
    .st-key-top_web_btn button { background: linear-gradient(135deg, #8b5cf6, #7c3aed) !important; }
    
    .main .block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1400px; }
    
    .hero-header {
        background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px 40px; border-radius: 16px; color: white;
        margin-bottom: 30px; box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3); position: relative; overflow: hidden;
    }
    .hero-title { font-size: 2.8rem; font-weight: 800; margin: 0; letter-spacing: -0.5px; position: relative; z-index: 2; }
    .hero-subtitle { font-size: 1.1rem; font-weight: 400; opacity: 0.95; margin-top: 10px; position: relative; z-index: 2; }
    .hero-badge { display: inline-block; background: rgba(255,255,255,0.2); padding: 6px 16px; border-radius: 20px; font-size: 0.85rem; font-weight: 500; margin-bottom: 15px; position: relative; z-index: 2; }
    
    .metric-card { background: linear-gradient(135deg, #1e1e2e, #2a2a3e); border: 1px solid rgba(102, 126, 234, 0.2); border-radius: 12px; padding: 20px; text-align: center; transition: all 0.3s ease; height: 100%; }
    .metric-card:hover { border-color: rgba(102, 126, 234, 0.6); transform: translateY(-4px); box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2); }
    .metric-value { font-size: 2.2rem; font-weight: 700; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin: 8px 0; }
    .metric-label { font-size: 0.85rem; color: #a0a0b0; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
    
    .feature-card { background: linear-gradient(135deg, #1a1a2e, #16213e); border-left: 4px solid #667eea; border-radius: 10px; padding: 20px; margin-bottom: 15px; transition: all 0.3s ease; }
    .feature-title { font-size: 1.1rem; font-weight: 600; color: #ffffff; margin-bottom: 6px; }
    .feature-desc { font-size: 0.9rem; color: #b0b0c0; line-height: 1.5; }
    
    .section-header { font-size: 1.5rem; font-weight: 700; color: #ffffff; margin: 30px 0 20px 0; padding-bottom: 10px; border-bottom: 2px solid rgba(102, 126, 234, 0.3); }
    
    .contact-card { background: linear-gradient(135deg, #1e1e2e, #2a2a3e); border: 1px solid rgba(102, 126, 234, 0.2); border-radius: 12px; padding: 18px; margin-bottom: 15px; }
    .contact-card .contact-icon { font-size: 1.8rem; margin-bottom: 8px; }
    .contact-card .contact-title { color: #ffffff; font-weight: 600; font-size: 1rem; margin-bottom: 5px; }
    .contact-card .contact-info { color: #b0b0c0; font-size: 0.88rem; line-height: 1.6; }
    .contact-card .contact-info strong { color: #10b981; font-size: 1rem; }
    .emergency-badge { display: inline-block; background: rgba(239, 68, 68, 0.2); color: #ef4444; padding: 3px 10px; border-radius: 8px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; }
    
    .gallery-card { background: linear-gradient(135deg, #1e1e2e, #2a2a3e); border: 1px solid rgba(102, 126, 234, 0.2); border-radius: 14px; overflow: hidden; margin-bottom: 20px; height: 100%; }
    .gallery-card:hover { border-color: rgba(102, 126, 234, 0.7); transform: translateY(-6px); }
    .gallery-image { width: 100%; height: 200px; object-fit: cover; display: block; }
    .gallery-body { padding: 18px 20px 22px 20px; }
    .gallery-category { display: inline-block; padding: 3px 10px; border-radius: 10px; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; background: rgba(102, 126, 234, 0.15); color: #667eea; margin-bottom: 10px; }
    .gallery-title { font-size: 1.15rem; font-weight: 700; color: #ffffff; margin-bottom: 8px; }
    .gallery-desc { font-size: 0.88rem; color: #b0b0c0; line-height: 1.5; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 6px !important; background: rgba(255, 255, 255, 0.03) !important; padding: 6px !important; border-radius: 12px !important; border-bottom: none !important; flex-wrap: wrap !important; }
    .stTabs [data-baseweb="tab"] { height: 44px !important; padding: 0 18px !important; border-radius: 10px !important; background: transparent !important; color: #b0b0c0 !important; font-weight: 500 !important; font-size: 0.88rem !important; border: none !important; }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #667eea, #764ba2) !important; color: #ffffff !important; font-weight: 600 !important; }
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { background: transparent !important; display: none !important; }
    
    .stButton > button { border-radius: 10px !important; font-weight: 500 !important; border: 1px solid rgba(102, 126, 234, 0.3) !important; }
    .stButton > button[kind="primary"] { background: linear-gradient(135deg, #667eea, #764ba2) !important; border: none !important; color: white !important; padding: 12px 24px !important; font-weight: 600 !important; }
    .stDownloadButton > button { background: linear-gradient(135deg, #10b981, #059669) !important; color: white !important; border: none !important; border-radius: 10px !important; padding: 12px 24px !important; font-weight: 600 !important; }
    
    .stNumberInput input, .stTextInput input { background: #1e1e2e !important; border: 1px solid rgba(102, 126, 234, 0.3) !important; border-radius: 8px !important; color: #ffffff !important; padding: 8px 12px !important; }
    .stNumberInput input:focus, .stTextInput input:focus { border-color: #667eea !important; }
    .stSelectbox > div > div { background: #1e1e2e !important; border: 1px solid rgba(102, 126, 234, 0.3) !important; border-radius: 8px !important; }
    div[data-testid="stForm"] { border: 1px solid rgba(102, 126, 234, 0.25) !important; border-radius: 14px !important; padding: 25px !important; background: rgba(30, 30, 46, 0.5) !important; }
    label { color: #d0d0e0 !important; font-weight: 500 !important; font-size: 0.9rem !important; }

    [data-testid="stStatusWidget"] {
        position: fixed !important; top: 50% !important; left: 50% !important; transform: translate(-50%, -50%) !important;
        z-index: 9999999 !important; background: rgba(30, 30, 46, 0.95) !important; padding: 25px 45px !important;
        border-radius: 16px !important; border: 2px solid #667eea !important; min-width: 220px !important;
    }
    [data-testid="stStatusWidget"] span { color: #ffffff !important; font-weight: 600 !important; font-size: 16px !important; }
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
    st.session_state.show_chat_page = True; st.rerun()
if st.button("📧", key="top_email_btn", help="Email Support"):
    st.session_state.show_email_page = True; st.rerun()
if st.button("🌐", key="top_web_btn", help="Visit Website"):
    st.session_state.show_website_page = True; st.rerun()


# ========================================
# HERO HEADER
# ========================================
st.markdown(f"""
<div class="hero-header">
    <div class="hero-badge">🏆 Final Year Project 2026</div>
    <h1 class="hero-title">🏥 MediFederate</h1>
    <p class="hero-subtitle">Welcome, <strong>{current_user['full_name']}</strong> ({role_label}) · Privacy-Preserving Multi-Disease Prediction Platform</p>
</div>
""", unsafe_allow_html=True)


# ========================================
# MAIN TABS
# ========================================
if is_patient:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "📈 Overview", "🩸 Diabetes", "❤️ Heart Disease", "🧠 Stroke",
        "🫘 Kidney", "🧬 Thyroid", "🩺 Live Prediction", "🏥 Gallery", "📞 Contacts"])
    tab10 = None
else:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
        "📈 Overview", "🩸 Diabetes", "❤️ Heart Disease", "🧠 Stroke",
        "🫘 Kidney", "🧬 Thyroid", "🩺 Live Prediction", "🏥 Gallery", "📞 Contacts", "📜 History"])


# ========================================
# TAB 1: OVERVIEW
# ========================================
with tab1:
    st.markdown('<div class="section-header">📊 Platform Performance Dashboard</div>', unsafe_allow_html=True)
    st.markdown("MediFederate enables multiple hospitals to collaboratively train AI models **without sharing any patient data**.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: ui.animated_metric_card("🩸", "Diabetes", "62.38%", "100,244 patients", "Beats Baseline", "success")
    with col2: ui.animated_metric_card("❤️", "Heart Disease", "88.52%", "303 patients", "⭐ Best", "warning")
    with col3: ui.animated_metric_card("🧠", "Stroke", "72.90%", "5,109 patients", "80% Recall", "info")
    with col4: ui.animated_metric_card("🫘", "Kidney", "100%", "400 patients", "🎯 Excellent", "success")
    with col5: ui.animated_metric_card("🧬", "Thyroid", "90.36%", "8,865 patients", "⭐ Improved", "success")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Model Comparison</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns([1, 1])
    with col_a:
        comparison = pd.DataFrame({
            "Disease": ["Diabetes", "Heart Disease", "Stroke", "Kidney Disease", "Thyroid"],
            "Accuracy (%)": [62.38, 88.52, 72.90, 100.00, 90.36],
            "Data Shared": ["0 B"]*5, "Privacy": ["✅ DP"]*5})
        st.dataframe(comparison, width='stretch', hide_index=True)
    with col_b:
        fig = ui.plotly_model_comparison(comparison)
        st.plotly_chart(fig, width='stretch', config={'displayModeBar': False}, key="overview_chart")
    
    st.success("✅ **5 diseases** predicted using real trained neural networks with Federated Learning + Differential Privacy — **ZERO patient data shared!**")


# ========================================
# TAB 2: DIABETES
# ========================================
with tab2:
    st.markdown('<div class="section-header">🩸 Diabetes Readmission Prediction</div>', unsafe_allow_html=True)
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1: st.metric("Accuracy", "62.38%", "+0.04% vs baseline")
    with col_info2: st.metric("Training Data", "100,244 patients")
    with col_info3: st.metric("Privacy", "✅ DP Enabled")
    st.markdown("---")
    
    with st.form("diabetes_form"):
        pat_info = render_patient_info("d")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age (Clinical)", min_value=5, max_value=95, value=55, step=1, key="d_age")
            time_hosp = st.number_input("Time in Hospital (days)", min_value=1, max_value=14, value=5, step=1, key="d_time")
            meds = st.number_input("Number of Medications", min_value=1, max_value=81, value=15, step=1, key="d_meds")
            lab = st.number_input("Lab Procedures", min_value=1, max_value=132, value=45, step=1, key="d_lab")
        with col2:
            diag = st.number_input("Number of Diagnoses", min_value=1, max_value=16, value=7, step=1, key="d_diag")
            proc = st.number_input("Procedures", min_value=0, max_value=6, value=2, step=1, key="d_proc")
            inpat = st.number_input("Previous Inpatient Visits", min_value=0, max_value=21, value=0, step=1, key="d_inpat")
            emerg = st.number_input("Previous Emergency Visits", min_value=0, max_value=76, value=0, step=1, key="d_emerg")
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔮 Predict Diabetes Risk", type="primary", width='stretch')
    
    if submitted:
        lp = st.empty()
        with lp.container(): ui.prediction_loading_animation("Diabetes")
        model = load_diabetes_model()
        data = {'age': age, 'time_in_hospital': time_hosp, 'num_medications': meds, 'num_lab_procedures': lab,
                'number_diagnoses': diag, 'num_procedures': proc, 'number_inpatient': inpat, 'number_emergency': emerg}
        prob = predict_with_model(model, data); lp.empty()
        
        if prob is not None:
            st.info(f"**Patient:** {pat_info['Patient Name']} · Age {age} · {time_hosp} days in hospital")
            pct = prob * 100
            ui.result_card_with_animation(prob > 0.5,
                "High Risk of Readmission" if prob > 0.5 else "Low Risk of Readmission", pct,
                "High probability of readmission. Close monitoring is recommended." if prob > 0.5 else "Low probability of readmission. Standard follow-up is sufficient.")
            hist.save_prediction("Diabetes", prob, "High Risk" if prob > 0.5 else "Low Risk",
                f"Patient: {pat_info['Patient Name']}, Age: {age}", user_email=user_email)
            report_data = dict(pat_info)
            report_data.update({"Age": age, "Time in Hospital (days)": time_hosp, "Number of Medications": meds,
                 "Lab Procedures": lab, "Number of Diagnoses": diag, "Procedures": proc,
                 "Previous Inpatient Visits": inpat, "Previous Emergency Visits": emerg})
            pdf_bytes = generate_medical_report("Diabetes", report_data,
                {"probability": prob, "is_high_risk": prob > 0.5, "summary": f"Patient has {pct:.1f}% probability of readmission."})
            st.download_button("📄  Download PDF Report", data=pdf_bytes,
                file_name=f"MediFederate_Diabetes_{pat_info['Patient Name'].replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf", width='stretch', key="d_download_btn")
        else: st.error("⚠️ Diabetes model not loaded.")


# ========================================
# TAB 3: HEART DISEASE
# ========================================
with tab3:
    st.markdown('<div class="section-header">❤️ Heart Disease Prediction</div>', unsafe_allow_html=True)
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1: st.metric("Accuracy", "88.52%", "⭐ Best Model")
    with col_info2: st.metric("Training Data", "303 patients")
    with col_info3: st.metric("Privacy", "✅ DP Enabled")
    st.markdown("---")
    
    with st.form("heart_form"):
        pat_info = render_patient_info("h")
        col1, col2 = st.columns(2)
        with col1:
            age_h = st.number_input("Age (Clinical)", min_value=20, max_value=90, value=55, step=1, key="h_age")
            sex_h = st.selectbox("Gender", ["Male", "Female"], key="h_sex")
            cp_h = st.selectbox("Chest Pain Type", [0, 1, 2, 3], format_func=lambda x: {0:"0 - Typical Angina",1:"1 - Atypical Angina",2:"2 - Non-anginal Pain",3:"3 - Asymptomatic"}[x], key="h_cp")
            trestbps = st.number_input("Resting BP (mm Hg)", min_value=90, max_value=200, value=130, step=1, key="h_bp")
            chol = st.number_input("Cholesterol (mg/dl)", min_value=100, max_value=600, value=240, step=1, key="h_chol")
            fbs = st.selectbox("Fasting Blood Sugar > 120", ["No", "Yes"], key="h_fbs")
        with col2:
            restecg = st.selectbox("Resting ECG", [0, 1, 2], format_func=lambda x: {0:"0 - Normal",1:"1 - ST-T Abnormality",2:"2 - LV Hypertrophy"}[x], key="h_ecg")
            thalach = st.number_input("Max Heart Rate", min_value=70, max_value=210, value=150, step=1, key="h_hr")
            exang = st.selectbox("Exercise Induced Angina", ["No", "Yes"], key="h_exang")
            oldpeak = st.number_input("ST Depression", min_value=0.0, max_value=7.0, value=1.0, step=0.1, key="h_old")
            slope = st.selectbox("Slope", [0, 1, 2], key="h_slope")
            ca = st.number_input("Major Vessels (0-3)", min_value=0, max_value=3, value=0, step=1, key="h_ca")
            thal = st.selectbox("Thalassemia", [1, 2, 3], key="h_thal")
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔮 Predict Heart Disease", type="primary", width='stretch')
    
    if submitted:
        lp = st.empty()
        with lp.container(): ui.prediction_loading_animation("Heart Disease")
        model = load_heart_model()
        data = {'age': age_h, 'sex': 1.0 if sex_h == "Male" else 0.0, 'cp': float(cp_h), 'trestbps': float(trestbps),
                'chol': float(chol), 'fbs': 1.0 if fbs == "Yes" else 0.0, 'restecg': float(restecg),
                'thalach': float(thalach), 'exang': 1.0 if exang == "Yes" else 0.0, 'oldpeak': float(oldpeak),
                'slope': float(slope), 'ca': float(ca), 'thal': float(thal)}
        prob = predict_with_model(model, data); lp.empty()
        
        if prob is not None:
            st.info(f"**Patient:** {pat_info['Patient Name']} · Age {age_h} · {sex_h} · BP {trestbps}")
            pct = prob * 100
            ui.result_card_with_animation(prob > 0.5,
                "High Risk of Heart Disease" if prob > 0.5 else "Low Risk of Heart Disease", pct,
                "Signs of heart disease. Further cardiac evaluation recommended." if prob > 0.5 else "Low risk for heart disease. Routine checkup sufficient.")
            hist.save_prediction("Heart Disease", prob, "High Risk" if prob > 0.5 else "Low Risk",
                f"Patient: {pat_info['Patient Name']}, Age: {age_h}, BP: {trestbps}", user_email=user_email)
            report_data = dict(pat_info)
            report_data.update({"Age": age_h, "Gender": sex_h, "Chest Pain Type": cp_h, "Resting BP (mm Hg)": trestbps,
                 "Cholesterol (mg/dl)": chol, "Fasting Blood Sugar > 120": fbs, "Resting ECG": restecg,
                 "Max Heart Rate": thalach, "Exercise Induced Angina": exang, "ST Depression": oldpeak,
                 "Slope": slope, "Major Vessels": ca, "Thalassemia": thal})
            pdf_bytes = generate_medical_report("Heart Disease", report_data,
                {"probability": prob, "is_high_risk": prob > 0.5, "summary": f"Patient has {pct:.1f}% probability of heart disease."})
            st.download_button("📄  Download PDF Report", data=pdf_bytes,
                file_name=f"MediFederate_Heart_{pat_info['Patient Name'].replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf", width='stretch', key="h_download_btn")
        else: st.error("⚠️ Heart model not loaded.")


# ========================================
# TAB 4: STROKE
# ========================================
with tab4:
    st.markdown('<div class="section-header">🧠 Stroke Prediction</div>', unsafe_allow_html=True)
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1: st.metric("Accuracy", "72.90%", "80% Recall")
    with col_info2: st.metric("Training Data", "5,109 patients")
    with col_info3: st.metric("Privacy", "✅ DP Enabled")
    st.markdown("---")
    
    with st.form("stroke_form"):
        pat_info = render_patient_info("s")
        col1, col2 = st.columns(2)
        with col1:
            age_s = st.number_input("Age (Clinical)", min_value=1, max_value=90, value=55, step=1, key="s_age")
            gender_s = st.selectbox("Gender", ["Male", "Female"], key="s_gender")
            hyp = st.selectbox("Hypertension", ["No", "Yes"], key="s_hyp")
            heart = st.selectbox("Heart Disease", ["No", "Yes"], key="s_heart")
            married = st.selectbox("Ever Married", ["No", "Yes"], key="s_mar")
        with col2:
            glucose = st.number_input("Average Glucose Level", min_value=50.0, max_value=300.0, value=100.0, step=0.1, key="s_gluc")
            bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0, step=0.1, key="s_bmi")
            work = st.selectbox("Work Type", ["Private", "Self-employed", "Govt_job", "children", "Never_worked"], key="s_work")
            residence = st.selectbox("Residence", ["Urban", "Rural"], key="s_res")
            smoking = st.selectbox("Smoking Status", ["never smoked", "formerly smoked", "smokes", "Unknown"], key="s_smoke")
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔮 Predict Stroke Risk", type="primary", width='stretch')
    
    if submitted:
        lp = st.empty()
        with lp.container(): ui.prediction_loading_animation("Stroke")
        model = load_stroke_model()
        data = {'gender': 1.0 if gender_s == "Male" else 0.0, 'age': float(age_s),
                'hypertension': 1.0 if hyp == "Yes" else 0.0, 'heart_disease': 1.0 if heart == "Yes" else 0.0,
                'ever_married': 1.0 if married == "Yes" else 0.0, 'Residence_type': 1.0 if residence == "Urban" else 0.0,
                'avg_glucose_level': float(glucose), 'bmi': float(bmi),
                'smoking_status': {'never smoked': 0.0, 'formerly smoked': 1.0, 'smokes': 2.0, 'Unknown': 3.0}[smoking]}
        for wt in ['Never_worked', 'Private', 'Self-employed', 'children']:
            data[f'work_type_{wt}'] = 1.0 if work == wt else 0.0
        prob = predict_with_model(model, data); lp.empty()
        
        if prob is not None:
            st.info(f"**Patient:** {pat_info['Patient Name']} · Age {age_s} · Glucose {glucose}")
            pct = prob * 100
            ui.result_card_with_animation(prob > 0.5,
                "High Risk of Stroke" if prob > 0.5 else "Low Risk of Stroke", pct,
                "High risk of stroke. Immediate medical consultation recommended." if prob > 0.5 else "Low risk of stroke. Maintain a healthy lifestyle.")
            hist.save_prediction("Stroke", prob, "High Risk" if prob > 0.5 else "Low Risk",
                f"Patient: {pat_info['Patient Name']}, Age: {age_s}, Glucose: {glucose}", user_email=user_email)
            report_data = dict(pat_info)
            report_data.update({"Age": age_s, "Gender": gender_s, "Hypertension": hyp, "Heart Disease": heart,
                 "Ever Married": married, "Average Glucose Level": glucose, "BMI": bmi,
                 "Work Type": work, "Residence": residence, "Smoking Status": smoking})
            pdf_bytes = generate_medical_report("Stroke", report_data,
                {"probability": prob, "is_high_risk": prob > 0.5, "summary": f"Patient has {pct:.1f}% probability of stroke."})
            st.download_button("📄  Download PDF Report", data=pdf_bytes,
                file_name=f"MediFederate_Stroke_{pat_info['Patient Name'].replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf", width='stretch', key="s_download_btn")
        else: st.error("⚠️ Stroke model not loaded.")


# ========================================
# TAB 5: KIDNEY DISEASE
# ========================================
with tab5:
    st.markdown('<div class="section-header">🫘 Kidney Disease Prediction</div>', unsafe_allow_html=True)
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1: st.metric("Accuracy", "100%", "🎯 Excellent")
    with col_info2: st.metric("Training Data", "400 patients")
    with col_info3: st.metric("Privacy", "✅ DP Enabled")
    st.markdown("---")
    
    with st.form("kidney_form"):
        pat_info = render_patient_info("k")
        col1, col2 = st.columns(2)
        with col1:
            age_k = st.number_input("Age (Clinical)", min_value=1, max_value=100, value=50, step=1, key="k_age")
            bp_k = st.number_input("Blood Pressure (mm Hg)", min_value=50, max_value=180, value=80, step=1, key="k_bp")
            sg_k = st.number_input("Specific Gravity", min_value=1.005, max_value=1.025, value=1.020, step=0.005, format="%.3f", key="k_sg")
            al_k = st.number_input("Albumin (0-5)", min_value=0, max_value=5, value=1, step=1, key="k_al")
            su_k = st.number_input("Sugar (0-5)", min_value=0, max_value=5, value=0, step=1, key="k_su")
            bgr_k = st.number_input("Blood Glucose Random", min_value=50, max_value=500, value=120, step=1, key="k_bgr")
            bu_k = st.number_input("Blood Urea", min_value=10, max_value=400, value=40, step=1, key="k_bu")
            sc_k = st.number_input("Serum Creatinine", min_value=0.5, max_value=20.0, value=1.2, step=0.1, key="k_sc")
            sod_k = st.number_input("Sodium", min_value=100, max_value=170, value=140, step=1, key="k_sod")
            pot_k = st.number_input("Potassium", min_value=2.0, max_value=50.0, value=4.5, step=0.1, key="k_pot")
        with col2:
            hemo_k = st.number_input("Hemoglobin", min_value=3.0, max_value=20.0, value=14.0, step=0.1, key="k_hemo")
            pcv_k = st.number_input("Packed Cell Volume", min_value=10, max_value=60, value=40, step=1, key="k_pcv")
            wc_k = st.number_input("White Blood Cell Count", min_value=2000, max_value=25000, value=8000, step=100, key="k_wc")
            rc_k = st.number_input("Red Blood Cell Count", min_value=2.0, max_value=8.0, value=5.0, step=0.1, key="k_rc")
            htn_k = st.selectbox("Hypertension", ["No", "Yes"], key="k_htn")
            dm_k = st.selectbox("Diabetes Mellitus", ["No", "Yes"], key="k_dm")
            cad_k = st.selectbox("Coronary Artery Disease", ["No", "Yes"], key="k_cad")
            appet_k = st.selectbox("Appetite", ["Good", "Poor"], key="k_appet")
            pe_k = st.selectbox("Pedal Edema", ["No", "Yes"], key="k_pe")
            ane_k = st.selectbox("Anemia", ["No", "Yes"], key="k_ane")
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔮 Predict Kidney Disease", type="primary", width='stretch')
    
    if submitted:
        lp = st.empty()
        with lp.container(): ui.prediction_loading_animation("Kidney Disease")
        model = load_kidney_model()
        data = {'age': float(age_k), 'bp': float(bp_k), 'sg': float(sg_k), 'al': float(al_k),
                'su': float(su_k), 'bgr': float(bgr_k), 'bu': float(bu_k), 'sc': float(sc_k),
                'sod': float(sod_k), 'pot': float(pot_k), 'hemo': float(hemo_k), 'pcv': float(pcv_k),
                'wc': float(wc_k), 'rc': float(rc_k),
                'htn': 1.0 if htn_k == "Yes" else 0.0, 'dm': 1.0 if dm_k == "Yes" else 0.0,
                'cad': 1.0 if cad_k == "Yes" else 0.0, 'appet': 1.0 if appet_k == "Good" else 0.0,
                'pe': 1.0 if pe_k == "Yes" else 0.0, 'ane': 1.0 if ane_k == "Yes" else 0.0,
                'rbc': 1.0, 'pc': 1.0, 'pcc': 0.0, 'ba': 0.0}
        prob = predict_with_model(model, data); lp.empty()
        
        if prob is not None:
            st.info(f"**Patient:** {pat_info['Patient Name']} · Age {age_k} · BP {bp_k} · Creatinine {sc_k}")
            pct = prob * 100
            ui.result_card_with_animation(prob > 0.5,
                "High Risk of Kidney Disease" if prob > 0.5 else "Low Risk of Kidney Disease", pct,
                "Signs of kidney disease. Immediate nephrology consultation recommended." if prob > 0.5 else "Low risk for kidney disease. Routine checkup sufficient.")
            hist.save_prediction("Kidney Disease", prob, "High Risk" if prob > 0.5 else "Low Risk",
                f"Patient: {pat_info['Patient Name']}, Age: {age_k}, Creatinine: {sc_k}", user_email=user_email)
            report_data = dict(pat_info)
            report_data.update({"Age": age_k, "Blood Pressure": bp_k, "Hemoglobin": hemo_k, "Serum Creatinine": sc_k,
                 "Blood Urea": bu_k, "Sodium": sod_k, "Potassium": pot_k,
                 "Hypertension": htn_k, "Diabetes": dm_k, "Anemia": ane_k})
            pdf_bytes = generate_medical_report("Kidney Disease", report_data,
                {"probability": prob, "is_high_risk": prob > 0.5, "summary": f"Patient has {pct:.1f}% probability of kidney disease."})
            st.download_button("📄  Download PDF Report", data=pdf_bytes,
                file_name=f"MediFederate_Kidney_{pat_info['Patient Name'].replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf", width='stretch', key="k_download_btn")
        else: st.error("⚠️ Kidney model not loaded.")


# ========================================
# TAB 6: THYROID DISEASE (UPDATED with 90.36% accuracy)
# ========================================
with tab6:
    st.markdown('<div class="section-header">🧬 Thyroid Disease Prediction</div>', unsafe_allow_html=True)
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1: st.metric("Accuracy", "90.36%", "⭐ Real Data")
    with col_info2: st.metric("Training Data", "8,865 patients")
    with col_info3: st.metric("Privacy", "✅ DP Enabled")
    st.markdown("---")
    
    with st.form("thyroid_form"):
        pat_info = render_patient_info("t")
        col1, col2, col3 = st.columns(3)
        with col1:
            t_age = st.number_input("Age (Clinical)", min_value=1, max_value=100, value=45, step=1, key="t_age")
            t_sex = st.selectbox("Gender", ["Female", "Male"], key="t_sex")
            t_tsh = st.number_input("TSH Level", min_value=0.0, max_value=50.0, value=2.0, step=0.1, key="t_tsh")
            t_t3 = st.number_input("T3 Level", min_value=0.0, max_value=10.0, value=1.5, step=0.1, key="t_t3")
            t_tt4 = st.number_input("TT4 Level", min_value=0.0, max_value=30.0, value=8.0, step=0.1, key="t_tt4")
            t_t4u = st.number_input("T4U Level", min_value=0.0, max_value=3.0, value=1.0, step=0.1, key="t_t4u")
            t_fti = st.number_input("FTI Level", min_value=0.0, max_value=30.0, value=8.0, step=0.1, key="t_fti")
            t_tbg = st.number_input("TBG Level", min_value=0.0, max_value=100.0, value=0.0, step=0.1, key="t_tbg")
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
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔮 Predict Thyroid Risk", type="primary", width='stretch')
    
    if submitted:
        lp = st.empty()
        with lp.container(): ui.prediction_loading_animation("Thyroid")
        model = load_thyroid_model()
        data = {
            'age': float(t_age), 'sex': 1.0 if t_sex == "Male" else 0.0,
            'on_thyroxine': 1.0 if t_on_thy == "Yes" else 0.0,
            'query_on_thyroxine': 1.0 if t_query_thy == "Yes" else 0.0,
            'on_antithyroid_meds': 1.0 if t_anti_thy == "Yes" else 0.0,
            'sick': 1.0 if t_sick == "Yes" else 0.0, 'pregnant': 1.0 if t_pregnant == "Yes" else 0.0,
            'thyroid_surgery': 1.0 if t_surgery == "Yes" else 0.0,
            'I131_treatment': 1.0 if t_i131 == "Yes" else 0.0,
            'query_hypothyroid': 1.0 if t_query_hypo == "Yes" else 0.0,
            'query_hyperthyroid': 1.0 if t_query_hyper == "Yes" else 0.0,
            'lithium': 1.0 if t_lithium == "Yes" else 0.0, 'goitre': 1.0 if t_goitre == "Yes" else 0.0,
            'tumor': 1.0 if t_tumor == "Yes" else 0.0, 'hypopituitary': 1.0 if t_hypopit == "Yes" else 0.0,
            'psych': 1.0 if t_psych == "Yes" else 0.0, 'TSH_measured': 1.0 if t_tsh_meas == "Yes" else 0.0,
            'TSH': float(t_tsh),
            'T3_measured': 1.0 if t_t3_meas == "Yes" else 0.0, 'T3': float(t_t3),
            'TT4_measured': 1.0 if t_tt4_meas == "Yes" else 0.0, 'TT4': float(t_tt4),
            'T4U_measured': 1.0 if t_t4u_meas == "Yes" else 0.0, 'T4U': float(t_t4u),
            'FTI_measured': 1.0 if t_fti_meas == "Yes" else 0.0, 'FTI': float(t_fti),
            'TBG_measured': 1.0 if t_tbg_meas == "Yes" else 0.0, 'TBG': float(t_tbg)
        }
        prob = predict_with_model(model, data); lp.empty()
        
        if prob is not None:
            st.info(f"**Patient:** {pat_info['Patient Name']} · Age {t_age} · TSH {t_tsh}")
            pct = prob * 100
            ui.result_card_with_animation(prob > 0.5,
                "High Risk of Thyroid Disease" if prob > 0.5 else "Low Risk of Thyroid Disease", pct,
                "High probability of thyroid disease. Endocrinology consultation recommended." if prob > 0.5 else "Low probability of thyroid disease. Routine follow-up sufficient.")
            hist.save_prediction("Thyroid", prob, "High Risk" if prob > 0.5 else "Low Risk",
                f"Patient: {pat_info['Patient Name']}, TSH: {t_tsh}, T3: {t_t3}", user_email=user_email)
            report_data = dict(pat_info)
            report_data.update({"Age": t_age, "Gender": t_sex, "TSH": t_tsh, "T3": t_t3, "TT4": t_tt4, "T4U": t_t4u, "FTI": t_fti, "TBG": t_tbg})
            pdf_bytes = generate_medical_report("Thyroid Disease", report_data,
                {"probability": prob, "is_high_risk": prob > 0.5, "summary": f"Patient has {pct:.1f}% probability of thyroid disease."})
            st.download_button("📄  Download PDF Report", data=pdf_bytes,
                file_name=f"MediFederate_Thyroid_{pat_info['Patient Name'].replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf", width='stretch', key="t_download_btn")
        else: st.error("⚠️ Thyroid model not loaded.")


# ========================================
# TAB 7: LIVE PREDICTION
# ========================================
with tab7:
    st.markdown('<div class="section-header">🩺 Live Patient Prediction</div>', unsafe_allow_html=True)
    st.markdown("Enter patient details below and get **real-time AI predictions** with downloadable report.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    disease_choice = st.selectbox("🏥 Select Disease",
        ["🩸 Diabetes", "❤️ Heart Disease", "🧠 Stroke", "🫘 Kidney Disease", "🧬 Thyroid"], key="api_disease_select")
    st.markdown("---")
    st.markdown("### 📝 Enter Patient Details")
    
    if disease_choice == "🩸 Diabetes":
        with st.form("api_diabetes_form"):
            pat_info = render_patient_info("api_d")
            col1, col2 = st.columns(2)
            with col1:
                api_d_age = st.number_input("Age (Clinical)", min_value=5, max_value=95, value=55, step=1, key="api_d_age")
                api_d_time = st.number_input("Time in Hospital (days)", min_value=1, max_value=14, value=5, step=1, key="api_d_time")
                api_d_meds = st.number_input("Number of Medications", min_value=1, max_value=81, value=15, step=1, key="api_d_meds")
                api_d_lab = st.number_input("Lab Procedures", min_value=1, max_value=132, value=45, step=1, key="api_d_lab")
            with col2:
                api_d_diag = st.number_input("Number of Diagnoses", min_value=1, max_value=16, value=7, step=1, key="api_d_diag")
                api_d_proc = st.number_input("Procedures", min_value=0, max_value=6, value=2, step=1, key="api_d_proc")
                api_d_inpat = st.number_input("Previous Inpatient Visits", min_value=0, max_value=21, value=0, step=1, key="api_d_inpat")
                api_d_emerg = st.number_input("Previous Emergency Visits", min_value=0, max_value=76, value=0, step=1, key="api_d_emerg")
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🚀 Get Prediction", type="primary", width='stretch')
        payload = {"age": api_d_age, "time_in_hospital": api_d_time, "num_medications": api_d_meds, "num_lab_procedures": api_d_lab, "number_diagnoses": api_d_diag, "num_procedures": api_d_proc, "number_inpatient": api_d_inpat, "number_emergency": api_d_emerg}
        endpoint = "diabetes"; disease_clean = "Diabetes"
        clinical_dict = {"Age": api_d_age, "Time in Hospital (days)": api_d_time, "Number of Medications": api_d_meds, "Lab Procedures": api_d_lab, "Number of Diagnoses": api_d_diag, "Procedures": api_d_proc, "Previous Inpatient Visits": api_d_inpat, "Previous Emergency Visits": api_d_emerg}

    elif disease_choice == "❤️ Heart Disease":
        with st.form("api_heart_form"):
            pat_info = render_patient_info("api_h")
            col1, col2 = st.columns(2)
            with col1:
                api_h_age = st.number_input("Age (Clinical)", min_value=20, max_value=90, value=55, step=1, key="api_h_age")
                api_h_sex = st.selectbox("Gender", ["Male", "Female"], key="api_h_sex")
                api_h_cp = st.selectbox("Chest Pain Type", [0, 1, 2, 3], format_func=lambda x: {0:"0 - Typical Angina",1:"1 - Atypical Angina",2:"2 - Non-anginal Pain",3:"3 - Asymptomatic"}[x], key="api_h_cp")
                api_h_bp = st.number_input("Resting BP (mm Hg)", min_value=90, max_value=200, value=130, step=1, key="api_h_bp")
                api_h_chol = st.number_input("Cholesterol (mg/dl)", min_value=100, max_value=600, value=240, step=1, key="api_h_chol")
                api_h_fbs = st.selectbox("Fasting Blood Sugar > 120", ["No", "Yes"], key="api_h_fbs")
            with col2:
                api_h_ecg = st.selectbox("Resting ECG", [0, 1, 2], format_func=lambda x: {0:"0 - Normal",1:"1 - ST-T Abnormality",2:"2 - LV Hypertrophy"}[x], key="api_h_ecg")
                api_h_hr = st.number_input("Max Heart Rate", min_value=70, max_value=210, value=150, step=1, key="api_h_hr")
                api_h_exang = st.selectbox("Exercise Induced Angina", ["No", "Yes"], key="api_h_exang")
                api_h_old = st.number_input("ST Depression", min_value=0.0, max_value=7.0, value=1.0, step=0.1, key="api_h_old")
                api_h_slope = st.selectbox("Slope", [0, 1, 2], key="api_h_slope")
                api_h_ca = st.number_input("Major Vessels (0-3)", min_value=0, max_value=3, value=0, step=1, key="api_h_ca")
                api_h_thal = st.selectbox("Thalassemia", [1, 2, 3], key="api_h_thal")
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🚀 Get Prediction", type="primary", width='stretch')
        payload = {"age": api_h_age, "sex": 1 if api_h_sex == "Male" else 0, "cp": api_h_cp, "trestbps": api_h_bp, "chol": api_h_chol, "fbs": 1 if api_h_fbs == "Yes" else 0, "restecg": api_h_ecg, "thalach": api_h_hr, "exang": 1 if api_h_exang == "Yes" else 0, "oldpeak": api_h_old, "slope": api_h_slope, "ca": api_h_ca, "thal": api_h_thal}
        endpoint = "heart"; disease_clean = "Heart Disease"
        clinical_dict = {"Age": api_h_age, "Gender": api_h_sex, "Chest Pain Type": api_h_cp, "Resting BP (mm Hg)": api_h_bp, "Cholesterol (mg/dl)": api_h_chol, "Fasting Blood Sugar > 120": api_h_fbs, "Resting ECG": api_h_ecg, "Max Heart Rate": api_h_hr, "Exercise Induced Angina": api_h_exang, "ST Depression": api_h_old, "Slope": api_h_slope, "Major Vessels": api_h_ca, "Thalassemia": api_h_thal}

    elif disease_choice == "🧠 Stroke":
        with st.form("api_stroke_form"):
            pat_info = render_patient_info("api_s")
            col1, col2 = st.columns(2)
            with col1:
                api_s_age = st.number_input("Age (Clinical)", min_value=1, max_value=90, value=55, step=1, key="api_s_age")
                api_s_gender = st.selectbox("Gender", ["Male", "Female"], key="api_s_gender")
                api_s_hyp = st.selectbox("Hypertension", ["No", "Yes"], key="api_s_hyp")
                api_s_heart = st.selectbox("Heart Disease", ["No", "Yes"], key="api_s_heart")
                api_s_mar = st.selectbox("Ever Married", ["No", "Yes"], key="api_s_mar")
            with col2:
                api_s_gluc = st.number_input("Average Glucose Level", min_value=50.0, max_value=300.0, value=100.0, step=0.1, key="api_s_gluc")
                api_s_bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0, step=0.1, key="api_s_bmi")
                api_s_work = st.selectbox("Work Type", ["Private", "Self-employed", "Govt_job", "children", "Never_worked"], key="api_s_work")
                api_s_res = st.selectbox("Residence", ["Urban", "Rural"], key="api_s_res")
                api_s_smoke = st.selectbox("Smoking Status", ["never smoked", "formerly smoked", "smokes", "Unknown"], key="api_s_smoke")
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🚀 Get Prediction", type="primary", width='stretch')
        payload = {"gender": 1 if api_s_gender == "Male" else 0, "age": api_s_age, "hypertension": 1 if api_s_hyp == "Yes" else 0, "heart_disease": 1 if api_s_heart == "Yes" else 0, "ever_married": 1 if api_s_mar == "Yes" else 0, "Residence_type": 1 if api_s_res == "Urban" else 0, "avg_glucose_level": api_s_gluc, "bmi": api_s_bmi, "smoking_status": {"never smoked": 0, "formerly smoked": 1, "smokes": 2, "Unknown": 3}[api_s_smoke], "work_type_Never_worked": 1 if api_s_work == "Never_worked" else 0, "work_type_Private": 1 if api_s_work == "Private" else 0, "work_type_Self-employed": 1 if api_s_work == "Self-employed" else 0, "work_type_children": 1 if api_s_work == "children" else 0}
        endpoint = "stroke"; disease_clean = "Stroke"
        clinical_dict = {"Age": api_s_age, "Gender": api_s_gender, "Hypertension": api_s_hyp, "Heart Disease": api_s_heart, "Ever Married": api_s_mar, "Average Glucose Level": api_s_gluc, "BMI": api_s_bmi, "Work Type": api_s_work, "Residence": api_s_res, "Smoking Status": api_s_smoke}

    elif disease_choice == "🫘 Kidney Disease":
        with st.form("api_kidney_form"):
            pat_info = render_patient_info("api_k")
            col1, col2 = st.columns(2)
            with col1:
                api_k_age = st.number_input("Age (Clinical)", min_value=1, max_value=100, value=50, step=1, key="api_k_age")
                api_k_bp = st.number_input("Blood Pressure", min_value=50, max_value=180, value=80, step=1, key="api_k_bp")
                api_k_sg = st.number_input("Specific Gravity", min_value=1.005, max_value=1.025, value=1.020, step=0.005, format="%.3f", key="api_k_sg")
                api_k_al = st.number_input("Albumin (0-5)", min_value=0, max_value=5, value=1, step=1, key="api_k_al")
                api_k_su = st.number_input("Sugar (0-5)", min_value=0, max_value=5, value=0, step=1, key="api_k_su")
                api_k_bgr = st.number_input("Blood Glucose Random", min_value=50, max_value=500, value=120, step=1, key="api_k_bgr")
                api_k_bu = st.number_input("Blood Urea", min_value=10, max_value=400, value=40, step=1, key="api_k_bu")
                api_k_sc = st.number_input("Serum Creatinine", min_value=0.5, max_value=20.0, value=1.2, step=0.1, key="api_k_sc")
                api_k_sod = st.number_input("Sodium", min_value=100, max_value=170, value=140, step=1, key="api_k_sod")
                api_k_pot = st.number_input("Potassium", min_value=2.0, max_value=50.0, value=4.5, step=0.1, key="api_k_pot")
            with col2:
                api_k_hemo = st.number_input("Hemoglobin", min_value=3.0, max_value=20.0, value=14.0, step=0.1, key="api_k_hemo")
                api_k_pcv = st.number_input("Packed Cell Volume", min_value=10, max_value=60, value=40, step=1, key="api_k_pcv")
                api_k_wc = st.number_input("White Blood Cell Count", min_value=2000, max_value=25000, value=8000, step=100, key="api_k_wc")
                api_k_rc = st.number_input("Red Blood Cell Count", min_value=2.0, max_value=8.0, value=5.0, step=0.1, key="api_k_rc")
                api_k_htn = st.selectbox("Hypertension", ["No", "Yes"], key="api_k_htn")
                api_k_dm = st.selectbox("Diabetes Mellitus", ["No", "Yes"], key="api_k_dm")
                api_k_cad = st.selectbox("Coronary Artery Disease", ["No", "Yes"], key="api_k_cad")
                api_k_appet = st.selectbox("Appetite", ["Good", "Poor"], key="api_k_appet")
                api_k_pe = st.selectbox("Pedal Edema", ["No", "Yes"], key="api_k_pe")
                api_k_ane = st.selectbox("Anemia", ["No", "Yes"], key="api_k_ane")
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🚀 Get Prediction", type="primary", width='stretch')
        payload = {"age": api_k_age, "bp": api_k_bp, "sg": api_k_sg, "al": api_k_al, "su": api_k_su, "bgr": api_k_bgr, "bu": api_k_bu, "sc": api_k_sc, "sod": api_k_sod, "pot": api_k_pot, "hemo": api_k_hemo, "pcv": api_k_pcv, "wc": api_k_wc, "rc": api_k_rc, "htn": 1 if api_k_htn == "Yes" else 0, "dm": 1 if api_k_dm == "Yes" else 0, "cad": 1 if api_k_cad == "Yes" else 0, "appet": 1 if api_k_appet == "Good" else 0, "pe": 1 if api_k_pe == "Yes" else 0, "ane": 1 if api_k_ane == "Yes" else 0, "rbc": 1, "pc": 1, "pcc": 0, "ba": 0}
        endpoint = "kidney"; disease_clean = "Kidney Disease"
        clinical_dict = {"Age": api_k_age, "Blood Pressure": api_k_bp, "Specific Gravity": api_k_sg, "Albumin": api_k_al, "Sugar": api_k_su, "Blood Glucose Random": api_k_bgr, "Blood Urea": api_k_bu, "Serum Creatinine": api_k_sc, "Sodium": api_k_sod, "Potassium": api_k_pot, "Hemoglobin": api_k_hemo, "Packed Cell Volume": api_k_pcv, "White Blood Cell Count": api_k_wc, "Red Blood Cell Count": api_k_rc, "Hypertension": api_k_htn, "Diabetes Mellitus": api_k_dm, "Coronary Artery Disease": api_k_cad, "Appetite": api_k_appet, "Pedal Edema": api_k_pe, "Anemia": api_k_ane}

    else:
        with st.form("api_thyroid_form"):
            pat_info = render_patient_info("api_t")
            col1, col2, col3 = st.columns(3)
            with col1:
                api_t_age = st.number_input("Age (Clinical)", min_value=1, max_value=100, value=45, step=1, key="api_t_age")
                api_t_sex = st.selectbox("Gender", ["Female", "Male"], key="api_t_sex")
                api_t_tsh = st.number_input("TSH Level", min_value=0.0, max_value=50.0, value=2.0, step=0.1, key="api_t_tsh")
                api_t_t3 = st.number_input("T3 Level", min_value=0.0, max_value=10.0, value=1.5, step=0.1, key="api_t_t3")
                api_t_tt4 = st.number_input("TT4 Level", min_value=0.0, max_value=30.0, value=8.0, step=0.1, key="api_t_tt4")
                api_t_t4u = st.number_input("T4U Level", min_value=0.0, max_value=3.0, value=1.0, step=0.1, key="api_t_t4u")
                api_t_fti = st.number_input("FTI Level", min_value=0.0, max_value=30.0, value=8.0, step=0.1, key="api_t_fti")
                api_t_tbg = st.number_input("TBG Level", min_value=0.0, max_value=100.0, value=0.0, step=0.1, key="api_t_tbg")
                api_t_on_thy = st.selectbox("On Thyroxine", ["No", "Yes"], key="api_t_on_thy")
            with col2:
                api_t_query_thy = st.selectbox("Query on Thyroxine", ["No", "Yes"], key="api_t_query_thy")
                api_t_anti_thy = st.selectbox("On Antithyroid Meds", ["No", "Yes"], key="api_t_anti_thy")
                api_t_sick = st.selectbox("Sick", ["No", "Yes"], key="api_t_sick")
                api_t_pregnant = st.selectbox("Pregnant", ["No", "Yes"], key="api_t_pregnant")
                api_t_surgery = st.selectbox("Thyroid Surgery", ["No", "Yes"], key="api_t_surgery")
                api_t_i131 = st.selectbox("I131 Treatment", ["No", "Yes"], key="api_t_i131")
                api_t_query_hypo = st.selectbox("Query Hypothyroid", ["No", "Yes"], key="api_t_query_hypo")
                api_t_query_hyper = st.selectbox("Query Hyperthyroid", ["No", "Yes"], key="api_t_query_hyper")
            with col3:
                api_t_lithium = st.selectbox("Lithium", ["No", "Yes"], key="api_t_lithium")
                api_t_goitre = st.selectbox("Goitre", ["No", "Yes"], key="api_t_goitre")
                api_t_tumor = st.selectbox("Tumor", ["No", "Yes"], key="api_t_tumor")
                api_t_hypopit = st.selectbox("Hypopituitary", ["No", "Yes"], key="api_t_hypopit")
                api_t_psych = st.selectbox("Psych", ["No", "Yes"], key="api_t_psych")
                api_t_tsh_meas = st.selectbox("TSH Measured", ["No", "Yes"], key="api_t_tsh_meas")
                api_t_t3_meas = st.selectbox("T3 Measured", ["No", "Yes"], key="api_t_t3_meas")
                api_t_tt4_meas = st.selectbox("TT4 Measured", ["No", "Yes"], key="api_t_tt4_meas")
                api_t_tbg_meas = st.selectbox("TBG Measured", ["No", "Yes"], key="api_t_tbg_meas")
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🚀 Get Prediction", type="primary", width='stretch')
        payload = {"age": api_t_age, "sex": 1 if api_t_sex == "Male" else 0, "TSH": api_t_tsh, "T3": api_t_t3, "TT4": api_t_tt4, "T4U": api_t_t4u, "FTI": api_t_fti, "TBG": api_t_tbg, "on_thyroxine": 1 if api_t_on_thy == "Yes" else 0, "query_on_thyroxine": 1 if api_t_query_thy == "Yes" else 0, "on_antithyroid_meds": 1 if api_t_anti_thy == "Yes" else 0, "sick": 1 if api_t_sick == "Yes" else 0, "pregnant": 1 if api_t_pregnant == "Yes" else 0, "thyroid_surgery": 1 if api_t_surgery == "Yes" else 0, "I131_treatment": 1 if api_t_i131 == "Yes" else 0, "query_hypothyroid": 1 if api_t_query_hypo == "Yes" else 0, "query_hyperthyroid": 1 if api_t_query_hyper == "Yes" else 0, "lithium": 1 if api_t_lithium == "Yes" else 0, "goitre": 1 if api_t_goitre == "Yes" else 0, "tumor": 1 if api_t_tumor == "Yes" else 0, "hypopituitary": 1 if api_t_hypopit == "Yes" else 0, "psych": 1 if api_t_psych == "Yes" else 0, "TSH_measured": 1 if api_t_tsh_meas == "Yes" else 0, "T3_measured": 1 if api_t_t3_meas == "Yes" else 0, "TT4_measured": 1 if api_t_tt4_meas == "Yes" else 0, "T4U_measured": 1, "FTI_measured": 1, "TBG_measured": 1 if api_t_tbg_meas == "Yes" else 0}
        endpoint = "thyroid"; disease_clean = "Thyroid"
        clinical_dict = {"Age": api_t_age, "Gender": api_t_sex, "TSH": api_t_tsh, "T3": api_t_t3, "TT4": api_t_tt4, "T4U": api_t_t4u, "FTI": api_t_fti, "TBG": api_t_tbg, "On Thyroxine": api_t_on_thy, "Query on Thyroxine": api_t_query_thy, "On Antithyroid Meds": api_t_anti_thy, "Sick": api_t_sick, "Pregnant": api_t_pregnant, "Thyroid Surgery": api_t_surgery, "I131 Treatment": api_t_i131, "Query Hypothyroid": api_t_query_hypo, "Query Hyperthyroid": api_t_query_hyper, "Lithium": api_t_lithium, "Goitre": api_t_goitre, "Tumor": api_t_tumor, "Hypopituitary": api_t_hypopit, "Psych": api_t_psych, "TSH Measured": api_t_tsh_meas, "T3 Measured": api_t_t3_meas, "TT4 Measured": api_t_tt4_meas}

    if submitted:
        with st.spinner(f"Generating prediction for {disease_clean}..."):
            try:
                import requests
                api_url = f"https://federated-diabetes-prediction-production.up.railway.app/predict/{endpoint}"
                response = requests.post(api_url, json=payload, timeout=60)
                if response.status_code == 200:
                    result = response.json()
                    st.session_state['api_result'] = result
                    st.session_state['api_disease_clean'] = disease_clean
                    st.session_state['api_patient_details'] = dict(pat_info)
                    st.session_state['api_clinical_details'] = clinical_dict
                    hist.save_prediction(disease_clean, result.get('probability', 0) / 100, result.get('risk_level', 'Unknown'), f"Patient: {pat_info['Patient Name']}", user_email=user_email)
                else:
                    st.error(f"❌ API returned error: {response.status_code}"); st.session_state['api_result'] = None
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")
                st.info("💡 Server may be waking up. Please wait 30 seconds and try again.")
                st.session_state['api_result'] = None
    
    if 'api_result' in st.session_state and st.session_state.get('api_result'):
        result = st.session_state['api_result']
        res_disease = st.session_state['api_disease_clean']
        p_details = st.session_state['api_patient_details']
        c_details = st.session_state['api_clinical_details']
        prob = result.get('probability', 0); risk = result.get('risk_level', 'Unknown')
        
        st.markdown("---")
        st.markdown("### 📊 Prediction Result")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if prob > 50: st.error("⚠️ **HIGH RISK DETECTED**")
        else: st.success("✅ **LOW RISK**")
        
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Patient</div><div class="metric-value" style="font-size: 1.2rem;">{p_details.get("Patient Name","N/A")}</div></div>', unsafe_allow_html=True)
        with col_r2:
            color = "#ef4444" if prob > 50 else "#10b981"
            st.markdown(f'<div class="metric-card"><div class="metric-label">Risk Level</div><div class="metric-value" style="color: {color}; font-size: 1.4rem;">{risk}</div></div>', unsafe_allow_html=True)
        with col_r3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Probability</div><div class="metric-value" style="font-size: 1.4rem;">{prob}%</div></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if prob > 50: st.warning("📋 **Clinical Note:** Elevated risk. Further clinical evaluation recommended.")
        else: st.info("📋 **Clinical Note:** Low risk. Standard follow-up sufficient.")
        st.success(f"🔒 **Privacy:** {result.get('data_shared', '0 bytes')} shared · DP Enabled")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🖨️ Print / Download Report")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            all_details = dict(p_details); all_details.update(c_details)
            pdf_bytes = generate_medical_report(res_disease, all_details,
                {"probability": prob / 100, "is_high_risk": prob > 50, "summary": f"Patient has {prob:.1f}% probability of {res_disease}."})
            st.download_button("📄  Download PDF Report", data=pdf_bytes,
                file_name=f"MediFederate_{res_disease.replace(' ', '_')}_{p_details.get('Patient Name','Patient').replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf", width='stretch', key="api_result_pdf")
        with col_p2:
            report_text = f"MEDIFEDERATE MEDICAL REPORT\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M')}\nDisease: {res_disease}\n\n"
            report_text += "=== PATIENT INFO ===\n"
            for k, v in p_details.items(): report_text += f"  {k}: {v}\n"
            report_text += "\n=== CLINICAL DATA ===\n"
            for k, v in c_details.items(): report_text += f"  {k}: {v}\n"
            report_text += f"\n=== RESULT ===\nProbability: {prob}%\nRisk Level: {risk}\n"
            st.download_button("📝  Download Text Report", data=report_text,
                file_name=f"MediFederate_{res_disease.replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain", width='stretch', key="api_result_txt")
        st.caption("✅ Prediction saved to history.")


# ========================================
# TAB 8: GALLERY
# ========================================
with tab8:
    st.markdown('<div class="section-header">🏥 Medical Knowledge Gallery</div>', unsafe_allow_html=True)
    gallery_items = [
        {"category": "CARDIOLOGY", "title": "Blood Pressure Monitoring", "desc": "High BP is a silent killer.", "image": "https://images.unsplash.com/photo-1579154204601-01588f351e67?w=800", "emoji": "💓", "query": "My blood pressure is high, what should I do?"},
        {"category": "CARDIOLOGY", "title": "Heart Health", "desc": "Cardiovascular disease is the #1 cause of death globally.", "image": "https://images.unsplash.com/photo-1628348070889-cb656235b4eb?w=800", "emoji": "❤️", "query": "I have chest pain, what should I do?"},
        {"category": "ENDOCRINOLOGY", "title": "Diabetes & Blood Sugar", "desc": "Monitor sugar regularly.", "image": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=800", "emoji": "🩸", "query": "My sugar level is 200, what should I do?"},
        {"category": "NEPHROLOGY", "title": "Kidney Health", "desc": "Stay hydrated and control BP.", "image": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=800", "emoji": "🫘", "query": "How can I keep my kidneys healthy?"},
        {"category": "NEUROLOGY", "title": "Stroke Awareness", "desc": "Remember FAST: Face, Arm, Speech, Time.", "image": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800", "emoji": "🧠", "query": "Tell me about stroke symptoms"},
        {"category": "ENDOCRINOLOGY", "title": "Thyroid Health", "desc": "Get TSH, T3, T4 checked if symptomatic.", "image": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=800", "emoji": "🧬", "query": "What are the symptoms of thyroid problems?"},
        {"category": "GENERAL HEALTH", "title": "Fever & Infections", "desc": "Fever is the body's defense against infection.", "image": "https://images.unsplash.com/photo-1584362917165-526a968579e8?w=800", "emoji": "🌡️", "query": "I have fever, what should I do?"},
        {"category": "EMERGENCY", "title": "Emergency Response", "desc": "Save these numbers: 1122, 115, 15, 1020.", "image": "https://images.unsplash.com/photo-1587745416684-47953f16f02f?w=800", "emoji": "🚨", "query": "What is the emergency number in Pakistan?"},
    ]
    for i in range(0, len(gallery_items), 2):
        col1, col2 = st.columns(2)
        for idx, col in [(i, col1), (i+1, col2)]:
            if idx < len(gallery_items):
                item = gallery_items[idx]
                with col:
                    st.markdown(f'<div class="gallery-card"><img src="{item["image"]}" class="gallery-image" onerror="this.style.display=\'none\'"/><div class="gallery-body"><span class="gallery-category">{item["category"]}</span><div class="gallery-title">{item["emoji"]} {item["title"]}</div><div class="gallery-desc">{item["desc"]}</div></div></div>', unsafe_allow_html=True)
                    if st.button(f"💬 Ask MediBot", key=f"gal_btn_{idx}", width='stretch'):
                        st.session_state.show_chat_page = True
                        st.session_state.pending_chat_query = item['query']
                        st.rerun()


# ========================================
# TAB 9: CONTACTS
# ========================================
with tab9:
    st.markdown('<div class="section-header">📞 Contacts & Helpline</div>', unsafe_allow_html=True)
    st.markdown("##### 🚨 Emergency Numbers")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown('<div class="contact-card"><div class="emergency-badge">Emergency</div><div class="contact-icon">🚨</div><div class="contact-title">Rescue</div><div class="contact-info"><strong>1122</strong></div></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="contact-card"><div class="emergency-badge">Ambulance</div><div class="contact-icon">🚑</div><div class="contact-title">Edhi</div><div class="contact-info"><strong>115</strong></div></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="contact-card"><div class="emergency-badge">Police</div><div class="contact-icon">👮</div><div class="contact-title">Police</div><div class="contact-info"><strong>15</strong></div></div>', unsafe_allow_html=True)
    with col4: st.markdown('<div class="contact-card"><div class="emergency-badge">Ambulance</div><div class="contact-icon">🚑</div><div class="contact-title">Chhipa</div><div class="contact-info"><strong>1020</strong></div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### 🏥 Major Hospitals")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="contact-card"><div class="contact-icon">🏥</div><div class="contact-title">Aga Khan University Hospital</div><div class="contact-info">📍 Karachi<br>📞 +92-21-111-911-911</div></div><div class="contact-card"><div class="contact-icon">🏥</div><div class="contact-title">Mayo Hospital</div><div class="contact-info">📍 Lahore<br>📞 +92-42-99211112</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="contact-card"><div class="contact-icon">🏥</div><div class="contact-title">Shaukat Khanum Memorial</div><div class="contact-info">📍 Lahore<br>📞 +92-42-35905000</div></div><div class="contact-card"><div class="contact-icon">🏥</div><div class="contact-title">PIMS Islamabad</div><div class="contact-info">📍 Islamabad<br>📞 +92-51-9261170</div></div>', unsafe_allow_html=True)


# ========================================
# TAB 10: HISTORY
# ========================================
if tab10 is not None:
    with tab10:
        st.markdown('<div class="section-header">📜 My Prediction History</div>', unsafe_allow_html=True)
        stats = hist.get_statistics(user_email=user_email)
        col1, col2, col3, col4 = st.columns(4)
        with col1: ui.animated_metric_card("📊", "Total", str(stats['total']))
        with col2: ui.animated_metric_card("🔴", "High Risk", str(stats['high_risk']))
        with col3: ui.animated_metric_card("🟢", "Low Risk", str(stats['low_risk']))
        with col4: ui.animated_metric_card("🏥", "Diseases", "5")
        st.markdown("<br>", unsafe_allow_html=True)
        col_f1, col_f2, col_f3 = st.columns([2, 2, 1])
        with col_f1:
            disease_filter = st.selectbox("🔍 Filter by Disease", ["All", "Diabetes", "Heart Disease", "Stroke", "Kidney Disease", "Thyroid"], key="hist_filter")
        with col_f2:
            csv_data = hist.export_to_csv(user_email=user_email)
            st.download_button("📥  Export CSV", data=csv_data,
                file_name=f"My_Predictions_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv", width='stretch', key="hist_export")
        with col_f3:
            if st.button("🗑️  Clear", width='stretch', key="hist_clear"):
                hist.clear_all_predictions(user_email=user_email); st.success("Cleared!"); st.rerun()
        df = hist.get_all_predictions(disease_filter=disease_filter, user_email=user_email)
        if not df.empty:
            display_df = df[['id', 'timestamp', 'disease', 'probability', 'risk_level']].copy()
            display_df['probability'] = (display_df['probability'] * 100).round(1).astype(str) + '%'
            st.dataframe(display_df, width='stretch', hide_index=True)
        else:
            st.info("📭 No predictions yet.")


# ========================================
# FOOTER
# ========================================
st.markdown("---")
col_l1, col_l2, col_l3 = st.columns(3)
with col_l1:
    if st.button("📋  Privacy Policy", width='stretch', key="footer_privacy"):
        st.session_state.show_privacy_page = True; st.rerun()
with col_l2:
    if st.button("📜  Terms of Service", width='stretch', key="footer_terms"):
        st.session_state.show_terms_page = True; st.rerun()
with col_l3:
    if st.button("📧  Contact Support", width='stretch', key="footer_contact"):
        st.session_state.show_email_page = True; st.rerun()

render_floating_chatbot()

st.markdown("---")
st.markdown(f'<div style="text-align: center; padding: 20px 0; color: #808090;"><p style="margin: 0; font-size: 0.9rem;">🎓 <strong>CS Final Year Project 2026</strong> · MediFederate Platform v2.0</p><p style="margin: 5px 0 0 0; font-size: 0.8rem;">Logged in as: <strong>{current_user["full_name"]}</strong> ({role_label})</p></div>', unsafe_allow_html=True)