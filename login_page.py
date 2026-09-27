"""
MediFederate Login Page
Professional Split-Screen Design with Guest Mode & Forgot Password
English only
"""

import streamlit as st
import auth


def inject_login_css():
    """Professional CSS for split-screen login page"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        section[data-testid="stSidebar"] { display: none !important; }
        
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .left-panel-content {
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 40px 35px;
            border-radius: 18px;
            color: white;
            min-height: 650px;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        .left-panel-content::before {
            content: "";
            position: absolute;
            top: -50%;
            right: -30%;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(255,255,255,0.08), transparent);
            border-radius: 50%;
        }
        
        .left-logo { font-size: 4rem; margin-bottom: 15px; position: relative; z-index: 2; }
        .left-title { font-size: 2.2rem; font-weight: 800; margin: 0 0 12px 0; letter-spacing: -0.5px; position: relative; z-index: 2; }
        .left-subtitle { font-size: 0.95rem; opacity: 0.9; line-height: 1.6; margin-bottom: 30px; position: relative; z-index: 2; }
        
        .feature-list { list-style: none; padding: 0; position: relative; z-index: 2; }
        .feature-list li { font-size: 0.92rem; margin-bottom: 12px; padding-left: 28px; position: relative; opacity: 0.95; }
        .feature-list li::before { content: "✓"; position: absolute; left: 0; font-weight: 700; color: #a5f3d0; font-size: 1.1rem; }
        
        .emergency-box {
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.4);
            border-radius: 12px;
            padding: 15px 18px;
            margin-top: 25px;
            position: relative;
            z-index: 2;
        }
        
        .emergency-box h4 { margin: 0 0 8px 0; font-size: 0.85rem; font-weight: 700; color: #ffcccc; text-transform: uppercase; letter-spacing: 1px; }
        .emergency-box p { margin: 4px 0; font-size: 0.85rem; opacity: 0.95; }
        .emergency-box .emergency-num { font-size: 1.2rem; font-weight: 800; color: #ffffff; }
        
        .form-header { text-align: center; margin-bottom: 20px; }
        .form-header-icon { font-size: 2.5rem; margin-bottom: 8px; }
        .form-header-title { font-size: 1.6rem; font-weight: 700; color: #ffffff; margin-bottom: 6px; }
        .form-header-subtitle { color: #a0a0b0; font-size: 0.85rem; }
        
        .patient-mode-card {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.1));
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 14px;
            padding: 18px;
            margin-bottom: 18px;
            text-align: center;
        }
        
        .patient-mode-card h4 { color: #10b981; font-size: 1rem; font-weight: 700; margin: 0 0 6px 0; }
        .patient-mode-card p { color: #a0e0c0; font-size: 0.83rem; margin: 0 0 12px 0; line-height: 1.5; }
        
        .st-key-patient_mode_btn button {
            background: linear-gradient(135deg, #10b981, #059669) !important;
            color: white !important;
            border: none !important;
            padding: 14px 24px !important;
            font-size: 1rem !important;
            font-weight: 700 !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4) !important;
            width: 100% !important;
        }
        
        .divider-text {
            text-align: center;
            color: #808090;
            font-size: 0.8rem;
            margin: 20px 0;
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
        
        .stTextInput label, .stSelectbox label {
            color: #e0e0e0 !important;
            font-weight: 500 !important;
            font-size: 0.88rem !important;
        }
        
        .stTextInput input, .stSelectbox select {
            background: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid rgba(102, 126, 234, 0.25) !important;
            border-radius: 10px !important;
            color: #ffffff !important;
            padding: 10px 14px !important;
            font-size: 0.9rem !important;
        }
        
        .stTextInput input:focus, .stSelectbox select:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15) !important;
        }
        
        .stButton > button {
            border-radius: 10px !important;
            font-weight: 600 !important;
            transition: all 0.25s ease !important;
            padding: 10px 20px !important;
            font-size: 0.95rem !important;
            width: 100% !important;
            border: 1px solid rgba(102, 126, 234, 0.3) !important;
        }
        
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 4px 14px rgba(102, 126, 234, 0.4) !important;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px !important;
            background: rgba(255, 255, 255, 0.03) !important;
            padding: 6px !important;
            border-radius: 12px !important;
            border-bottom: none !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 42px !important;
            border-radius: 10px !important;
            background: transparent !important;
            color: #b0b0c0 !important;
            font-weight: 500 !important;
            font-size: 0.88rem !important;
            border: none !important;
            flex-grow: 1 !important;
            justify-content: center !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            color: #ffffff !important;
            box-shadow: 0 4px 14px rgba(102, 126, 234, 0.35) !important;
            font-weight: 600 !important;
        }
        
        .stTabs [data-baseweb="tab-highlight"],
        .stTabs [data-baseweb="tab-border"] {
            display: none !important;
        }
        
        .support-footer {
            text-align: center;
            margin-top: 15px;
            padding-top: 12px;
            border-top: 1px solid rgba(102, 126, 234, 0.15);
        }
        
        .support-footer p { color: #808090; font-size: 0.8rem; margin: 4px 0; }
    </style>
    """, unsafe_allow_html=True)


def render_login_page():
    """Render the split-screen login page with guest mode"""
    inject_login_css()
    
    if 'show_forgot_password' not in st.session_state:
        st.session_state.show_forgot_password = False
    
    if st.session_state.show_forgot_password:
        render_forgot_password_form()
        return
    
    left_col, right_col = st.columns([1, 1], gap="large")
    
    # ============ LEFT PANEL ============
    with left_col:
        st.markdown("""<div class="left-panel-content"><div class="left-logo">🏥</div><div class="left-title">MediFederate</div><div class="left-subtitle">Privacy-Preserving Multi-Disease Prediction Platform powered by Federated Learning + Differential Privacy</div><ul class="feature-list"><li>AI-powered disease prediction</li><li>Zero patient data sharing</li><li>Explainable AI (SHAP analysis)</li><li>PDF medical reports</li><li>24/7 AI health chatbot</li></ul><div class="emergency-box"><h4>🚨 Emergency Contacts</h4><p>Rescue: <span class="emergency-num">1122</span></p><p>Edhi Ambulance: <span class="emergency-num">115</span></p><p>Police: <span class="emergency-num">15</span></p></div></div>""", unsafe_allow_html=True)
    
    # ============ RIGHT PANEL ============
    with right_col:
        st.markdown("""
        <div class="form-header">
            <div class="form-header-icon">🔐</div>
            <div class="form-header-title">Welcome to MediFederate</div>
            <div class="form-header-subtitle">Sign in to access your healthcare dashboard</div>
        </div>
        """, unsafe_allow_html=True)
        
        # ===== PATIENT MODE =====
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
        
        st.markdown('<div class="divider-text">For Doctors & Medical Staff</div>', unsafe_allow_html=True)
        
        # ===== DOCTOR LOGIN/SIGNUP TABS =====
        tab_login, tab_signup = st.tabs(["🔐  Doctor Login", "✨  Register"])
        
        with tab_login:
            with st.form("login_form", clear_on_submit=False):
                st.markdown("#### Welcome Back 👨‍⚕️")
                
                email = st.text_input("📧 Email Address", placeholder="doctor@hospital.com", key="login_email")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password", key="login_password")
                
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
            
            if st.button("🔑  Forgot Password?", use_container_width=True, key="forgot_pass_btn"):
                st.session_state.show_forgot_password = True
                st.rerun()
        
        with tab_signup:
            with st.form("signup_form", clear_on_submit=False):
                st.markdown("#### Register as Doctor 👨‍⚕️")
                
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
        
        # ===== SUPPORT SECTION =====
        st.markdown("""
        <div class="support-footer">
            <p>📞 Helpline: <strong>042-111-222-333</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        col_email, col_web = st.columns(2)
        
        with col_email:
            if st.button("📧 Email Support", use_container_width=True, key="login_email_btn"):
                st.session_state.show_email_page = True
                st.session_state.show_website_page = False
                st.session_state.show_privacy_page = False
                st.session_state.show_terms_page = False
                st.rerun()
        
        with col_web:
            if st.button("🌐 Visit Website", use_container_width=True, key="login_web_btn"):
                st.session_state.show_website_page = True
                st.session_state.show_email_page = False
                st.session_state.show_privacy_page = False
                st.session_state.show_terms_page = False
                st.rerun()
        
        # ===== LEGAL LINKS =====
        col_p, col_t = st.columns(2)
        
        with col_p:
            if st.button("📋 Privacy Policy", use_container_width=True, key="login_privacy_btn"):
                st.session_state.show_privacy_page = True
                st.session_state.show_email_page = False
                st.session_state.show_website_page = False
                st.session_state.show_terms_page = False
                st.rerun()
        
        with col_t:
            if st.button("📜 Terms of Service", use_container_width=True, key="login_terms_btn"):
                st.session_state.show_terms_page = True
                st.session_state.show_email_page = False
                st.session_state.show_website_page = False
                st.session_state.show_privacy_page = False
                st.rerun()
        
        st.markdown("""
        <div class="support-footer" style="margin-top: 10px; border-top: none;">
            <p>🎓 CS Final Year Project 2026</p>
        </div>
        """, unsafe_allow_html=True)


def render_forgot_password_form():
    """Render forgot password reset form"""
    inject_login_css()
    
    left_space, center_col, right_space = st.columns([1, 2, 1])
    
    with center_col:
        st.markdown("""
        <div class="form-header" style="margin-top: 40px;">
            <div class="form-header-icon">🔑</div>
            <div class="form-header-title">Reset Your Password</div>
            <div class="form-header-subtitle">Enter your registered email and set a new password</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: rgba(59, 130, 246, 0.1); border-left: 4px solid #3b82f6; border-radius: 10px; padding: 14px 18px; margin-bottom: 20px; color: #93c5fd; font-size: 0.85rem; line-height: 1.6;">
            <strong>ℹ️ Note:</strong> This is a demo password reset. In a real system, you would receive a verification email first.
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("forgot_password_form", clear_on_submit=False):
            email = st.text_input("📧 Registered Email", placeholder="doctor@hospital.com", key="fp_email")
            new_password = st.text_input("🔒 New Password", type="password", placeholder="Minimum 6 characters", key="fp_new_pass")
            confirm_password = st.text_input("🔒 Confirm New Password", type="password", placeholder="Re-enter new password", key="fp_confirm_pass")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            submit = st.form_submit_button("🔑  Reset Password", type="primary", use_container_width=True)
            
            if submit:
                if not email or not new_password or not confirm_password:
                    st.error("⚠️ Please fill all fields.")
                elif new_password != confirm_password:
                    st.error("⚠️ Passwords do not match.")
                elif len(new_password) < 6:
                    st.error("⚠️ Password must be at least 6 characters.")
                else:
                    success, message = auth.reset_password(email, new_password)
                    if success:
                        st.success(f"✅ {message}")
                        st.info("🔄 Redirecting to login...")
                        st.session_state.show_forgot_password = False
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("←  Back to Login", use_container_width=True, key="back_to_login_btn"):
            st.session_state.show_forgot_password = False
            st.rerun()


def logout():
    """Logout the current user"""
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.show_chat_page = False
    st.session_state.pending_chat_query = None
    st.session_state.show_email_page = False
    st.session_state.show_website_page = False
    st.session_state.show_privacy_page = False
    st.session_state.show_terms_page = False
    st.session_state.show_forgot_password = False
    st.session_state.welcome_toast_shown = False
    st.rerun()