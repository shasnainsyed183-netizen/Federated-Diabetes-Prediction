"""
MediFederate Login Page
Professional Split-Screen Design with Guest Mode
Inspired by MyChart (Epic) and Apex Health
"""

import streamlit as st
import auth


def inject_login_css():
    """Professional CSS for split-screen login page"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
            margin: 0 !important;
        }
        
        /* Split Screen Container */
        .split-container {
            display: flex;
            min-height: 100vh;
        }
        
        /* Left Panel - Branding */
        .left-panel {
            flex: 1;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 60px 50px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            color: white;
            position: relative;
            overflow: hidden;
        }
        
        .left-panel::before {
            content: "";
            position: absolute;
            top: -50%;
            right: -20%;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
            border-radius: 50%;
        }
        
        .left-logo {
            font-size: 5rem;
            margin-bottom: 20px;
            position: relative;
            z-index: 2;
        }
        
        .left-title {
            font-size: 2.8rem;
            font-weight: 800;
            margin: 0 0 15px 0;
            letter-spacing: -0.5px;
            position: relative;
            z-index: 2;
        }
        
        .left-subtitle {
            font-size: 1.1rem;
            opacity: 0.9;
            line-height: 1.6;
            margin-bottom: 40px;
            position: relative;
            z-index: 2;
        }
        
        .feature-list {
            list-style: none;
            padding: 0;
            position: relative;
            z-index: 2;
        }
        
        .feature-list li {
            font-size: 1rem;
            margin-bottom: 15px;
            padding-left: 32px;
            position: relative;
            opacity: 0.95;
        }
        
        .feature-list li::before {
            content: "✓";
            position: absolute;
            left: 0;
            font-weight: 700;
            color: #a5f3d0;
            font-size: 1.2rem;
        }
        
        /* Emergency Box on Left */
        .emergency-box {
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.4);
            border-radius: 12px;
            padding: 18px 22px;
            margin-top: 40px;
            position: relative;
            z-index: 2;
            backdrop-filter: blur(10px);
        }
        
        .emergency-box h4 {
            margin: 0 0 10px 0;
            font-size: 0.95rem;
            font-weight: 700;
            color: #ffcccc;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .emergency-box p {
            margin: 4px 0;
            font-size: 0.9rem;
            opacity: 0.95;
        }
        
        .emergency-box .emergency-num {
            font-size: 1.4rem;
            font-weight: 800;
            color: #ffffff;
        }
        
        /* Right Panel - Form */
        .right-panel {
            flex: 1;
            background: #0f0f1a;
            padding: 60px 50px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            overflow-y: auto;
        }
        
        .form-wrapper {
            max-width: 420px;
            margin: 0 auto;
            width: 100%;
        }
        
        .form-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .form-header-icon {
            font-size: 3rem;
            margin-bottom: 10px;
        }
        
        .form-header-title {
            font-size: 1.8rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 6px;
        }
        
        .form-header-subtitle {
            color: #a0a0b0;
            font-size: 0.9rem;
        }
        
        /* Patient Mode Card */
        .patient-mode-card {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 14px;
            padding: 22px;
            margin-bottom: 25px;
            text-align: center;
        }
        
        .patient-mode-card h4 {
            color: #10b981;
            font-size: 1.1rem;
            font-weight: 700;
            margin: 0 0 8px 0;
        }
        
        .patient-mode-card p {
            color: #a0e0c0;
            font-size: 0.88rem;
            margin: 0 0 15px 0;
            line-height: 1.5;
        }
        
        .st-key-patient_mode_btn button {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
            color: white !important;
            border: none !important;
            padding: 14px 24px !important;
            font-size: 1rem !important;
            font-weight: 700 !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4) !important;
            transition: all 0.25s ease !important;
            width: 100% !important;
        }
        
        .st-key-patient_mode_btn button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 22px rgba(16, 185, 129, 0.6) !important;
        }
        
        /* Divider */
        .divider-text {
            text-align: center;
            color: #808090;
            font-size: 0.85rem;
            margin: 25px 0;
            position: relative;
        }
        
        .divider-text::before,
        .divider-text::after {
            content: "";
            position: absolute;
            top: 50%;
            width: 35%;
            height: 1px;
            background: rgba(102, 126, 234, 0.2);
        }
        
        .divider-text::before { left: 0; }
        .divider-text::after { right: 0; }
        
        /* Form Inputs */
        .stTextInput label, .stSelectbox label {
            color: #e0e0e0 !important;
            font-weight: 500 !important;
            font-size: 0.9rem !important;
        }
        
        .stTextInput input, .stSelectbox select {
            background: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid rgba(102, 126, 234, 0.25) !important;
            border-radius: 10px !important;
            color: #ffffff !important;
            padding: 12px 14px !important;
            font-size: 0.95rem !important;
        }
        
        .stTextInput input:focus, .stSelectbox select:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15) !important;
        }
        
        /* Buttons */
        .stButton > button {
            border-radius: 10px !important;
            font-weight: 600 !important;
            transition: all 0.25s ease !important;
            padding: 12px 24px !important;
            font-size: 1rem !important;
            width: 100% !important;
            border: 1px solid rgba(102, 126, 234, 0.3) !important;
        }
        
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 4px 14px rgba(102, 126, 234, 0.4) !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 22px rgba(102, 126, 234, 0.6) !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px !important;
            background: rgba(255, 255, 255, 0.03) !important;
            padding: 6px !important;
            border-radius: 12px !important;
            border-bottom: none !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 44px !important;
            border-radius: 10px !important;
            background: transparent !important;
            color: #b0b0c0 !important;
            font-weight: 500 !important;
            font-size: 0.9rem !important;
            border: none !important;
            flex-grow: 1 !important;
            justify-content: center !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: #ffffff !important;
            box-shadow: 0 4px 14px rgba(102, 126, 234, 0.35) !important;
            font-weight: 600 !important;
        }
        
        .stTabs [data-baseweb="tab-highlight"] {
            display: none !important;
        }
        
        .stTabs [data-baseweb="tab-border"] {
            display: none !important;
        }
        
        /* Support Footer */
        .support-footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid rgba(102, 126, 234, 0.15);
        }
        
        .support-footer p {
            color: #808090;
            font-size: 0.82rem;
            margin: 5px 0;
        }
        
        .support-footer a {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            .split-container {
                flex-direction: column;
            }
            .left-panel {
                padding: 40px 30px;
                min-height: auto;
            }
            .left-title {
                font-size: 2rem;
            }
            .right-panel {
                padding: 40px 30px;
            }
        }
    </style>
    """, unsafe_allow_html=True)


def render_login_page():
    """Render the split-screen login page with guest mode"""
    inject_login_css()
    
    # Two columns for split screen
    left_col, right_col = st.columns([1, 1], gap="small")
    
    # ============ LEFT PANEL: BRANDING ============
    with left_col:
        st.markdown("""
        <div class="left-panel">
            <div class="left-logo">🏥</div>
            <div class="left-title">MediFederate</div>
            <div class="left-subtitle">
                Privacy-Preserving Multi-Disease Prediction Platform
                powered by Federated Learning + Differential Privacy
            </div>
            
            <ul class="feature-list">
                <li>AI-powered disease prediction</li>
                <li>Zero patient data sharing</li>
                <li>Explainable AI (SHAP analysis)</li>
                <li>PDF medical reports</li>
                <li>24/7 AI health chatbot</li>
            </ul>
            
            <div class="emergency-box">
                <h4>🚨 Emergency Contacts</h4>
                <p>Rescue: <span class="emergency-num">1122</span></p>
                <p>Edhi Ambulance: <span class="emergency-num">115</span></p>
                <p>Police: <span class="emergency-num">15</span></p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ============ RIGHT PANEL: LOGIN FORM ============
    with right_col:
        st.markdown('<div class="right-panel">', unsafe_allow_html=True)
        st.markdown('<div class="form-wrapper">', unsafe_allow_html=True)
        
        # Form Header
        st.markdown("""
        <div class="form-header">
            <div class="form-header-icon">🔐</div>
            <div class="form-header-title">Welcome to MediFederate</div>
            <div class="form-header-subtitle">Sign in to access your healthcare dashboard</div>
        </div>
        """, unsafe_allow_html=True)
        
        # ===== PATIENT MODE (Guest) =====
        st.markdown("""
        <div class="patient-mode-card">
            <h4>👤 Are you a Patient?</h4>
            <p>No login needed! Get instant access to AI health predictions, chatbot, and PDF reports.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("👤  Continue as Patient (Guest)", use_container_width=True, key="patient_mode_btn"):
            st.session_state.logged_in = True
            st.session_state.user = {
                'id': None,
                'full_name': 'Patient (Guest)',
                'email': 'guest@medifederate',
                'role': 'patient',
                'hospital': 'N/A'
            }
            st.rerun()
        
        # Divider
        st.markdown('<div class="divider-text">For Doctors & Medical Staff</div>', unsafe_allow_html=True)
        
        # ===== DOCTOR LOGIN/SIGNUP TABS =====
        tab_login, tab_signup = st.tabs(["🔐  Doctor Login", "✨  Register"])
        
        # Login Tab
        with tab_login:
            with st.form("login_form", clear_on_submit=False):
                st.markdown("#### Welcome Back 👨‍⚕️")
                st.markdown("<p style='color: #a0a0b0; font-size: 0.85rem; margin-top: -8px;'>Sign in to your doctor account</p>", unsafe_allow_html=True)
                
                email = st.text_input("📧 Email Address", placeholder="doctor@hospital.com", key="login_email")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password", key="login_password")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                submit = st.form_submit_button("🔐  Sign In as Doctor", type="primary", use_container_width=True)
                
                if submit:
                    if not email or not password:
                        st.error("⚠️ Please enter both email and password.")
                    else:
                        success, message, user_data = auth.login(email, password)
                        
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.user = user_data
                            st.success(f"✅ Welcome back, {user_data['full_name']}!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
        
        # Signup Tab
        with tab_signup:
            with st.form("signup_form", clear_on_submit=False):
                st.markdown("#### Register as Doctor 👨‍⚕️")
                st.markdown("<p style='color: #a0a0b0; font-size: 0.85rem; margin-top: -8px;'>Create your doctor account</p>", unsafe_allow_html=True)
                
                full_name = st.text_input("👤 Full Name", placeholder="Dr. Ahmed Khan", key="signup_name")
                email_s = st.text_input("📧 Email Address", placeholder="doctor@hospital.com", key="signup_email")
                password_s = st.text_input("🔒 Password", type="password", placeholder="Minimum 6 characters", key="signup_password")
                password_confirm = st.text_input("🔒 Confirm Password", type="password", placeholder="Re-enter your password", key="signup_confirm")
                
                hospital = st.selectbox(
                    "🏥 Hospital / Institution",
                    [
                        "Aga Khan University Hospital",
                        "Shaukat Khanum Memorial Hospital",
                        "Mayo Hospital Lahore",
                        "Jinnah Postgraduate Medical Centre",
                        "Services Hospital Lahore",
                        "PIMS Islamabad",
                        "Other / Private Practice",
                    ],
                    key="signup_hospital"
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                submit_s = st.form_submit_button("✨  Create Doctor Account", type="primary", use_container_width=True)
                
                if submit_s:
                    if not full_name or not email_s or not password_s or not password_confirm:
                        st.error("⚠️ Please fill in all fields.")
                    elif password_s != password_confirm:
                        st.error("⚠️ Passwords do not match.")
                    elif len(password_s) < 6:
                        st.error("⚠️ Password must be at least 6 characters.")
                    else:
                        success, message, user_data = auth.signup(
                            full_name, email_s, password_s, hospital
                        )
                        
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.user = user_data
                            st.success(f"✅ Account created! Welcome, {user_data['full_name']}!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
        
        # Support Footer
        st.markdown("""
        <div class="support-footer">
            <p>📞 Helpline: <strong>042-111-222-333</strong></p>
            <p>📧 Email: <a href="mailto:support@medifederate.com">support@medifederate.com</a></p>
            <p>🌐 www.medifederate.com</p>
            <p style="margin-top: 15px;">🎓 CS Final Year Project 2026</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div></div>', unsafe_allow_html=True)


def logout():
    """Logout the current user"""
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.show_chat_page = False
    st.session_state.pending_chat_query = None
    st.rerun()