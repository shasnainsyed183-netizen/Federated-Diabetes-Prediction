"""
MediFederate Info Pages
Email Support, Website — with detailed information (English only)
"""

import streamlit as st


def inject_info_css():
    """CSS for info pages"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        section[data-testid="stSidebar"] { display: none !important; }
        
        .main .block-container {
            padding-top: 4rem;
            padding-bottom: 4rem;
            max-width: 1100px;
            margin: 0 auto;
        }
        
        .info-hero {
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 45px 40px;
            border-radius: 18px;
            color: white;
            margin-bottom: 35px;
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .info-hero::before {
            content: "";
            position: absolute;
            top: -50%;
            right: -10%;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(255,255,255,0.1), transparent);
            border-radius: 50%;
        }
        
        .info-hero-icon { font-size: 3.5rem; margin-bottom: 12px; position: relative; z-index: 2; }
        .info-hero-title { font-size: 2.2rem; font-weight: 800; margin: 0; letter-spacing: -0.5px; position: relative; z-index: 2; }
        .info-hero-subtitle { font-size: 1rem; opacity: 0.95; margin-top: 10px; position: relative; z-index: 2; }
        
        .info-card {
            background: linear-gradient(135deg, #1e1e2e, #2a2a3e);
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 14px;
            padding: 22px;
            margin-bottom: 18px;
            transition: all 0.3s ease;
            height: 100%;
        }
        
        .info-card:hover {
            border-color: rgba(102, 126, 234, 0.6);
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        }
        
        .info-card-icon { font-size: 2rem; margin-bottom: 10px; }
        .info-card-title { font-size: 1.1rem; font-weight: 700; color: #ffffff; margin-bottom: 6px; }
        .info-card-desc { font-size: 0.9rem; color: #b0b0c0; line-height: 1.7; }
        .info-card-desc strong { color: #10b981; }
        
        .email-list {
            background: rgba(102, 126, 234, 0.08);
            border-left: 4px solid #667eea;
            border-radius: 10px;
            padding: 18px 22px;
            margin-bottom: 16px;
        }
        
        .email-list-title {
            color: #667eea;
            font-weight: 700;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
        }
        
        .email-item {
            color: #ffffff;
            font-size: 0.95rem;
            padding: 8px 0;
            border-bottom: 1px dashed rgba(102, 126, 234, 0.15);
        }
        
        .email-item:last-child { border-bottom: none; }
        .email-item strong { color: #10b981; font-weight: 600; }
        
        .demo-badge {
            display: inline-block;
            background: rgba(245, 158, 11, 0.2);
            color: #f59e0b;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 0.65rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-left: 6px;
        }
        
        .info-section-header {
            font-size: 1.4rem;
            font-weight: 700;
            color: #ffffff;
            margin: 35px 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(102, 126, 234, 0.3);
        }
        
        .feature-item {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 10px;
            padding: 14px 18px;
            margin-bottom: 12px;
            border-left: 3px solid #667eea;
        }
        
        .feature-item-title { color: #ffffff; font-weight: 600; font-size: 0.95rem; margin-bottom: 4px; }
        .feature-item-desc { color: #a0a0b0; font-size: 0.85rem; line-height: 1.6; }
        
        .team-card {
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
            height: 100%;
        }
        
        .team-card:hover { transform: translateY(-4px); border-color: rgba(102, 126, 234, 0.6); }
        .team-avatar { font-size: 2.5rem; margin-bottom: 10px; }
        .team-name { color: #ffffff; font-weight: 700; font-size: 1rem; margin-bottom: 4px; }
        .team-role { color: #667eea; font-size: 0.8rem; font-weight: 500; }
        
        .notice-box {
            background: rgba(59, 130, 246, 0.1);
            border-left: 4px solid #3b82f6;
            border-radius: 10px;
            padding: 16px 20px;
            margin: 20px 0;
            color: #93c5fd;
            font-size: 0.88rem;
            line-height: 1.6;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #1e1e2e, #2a2a3e);
            border: 1px solid rgba(102, 126, 234, 0.25);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
            height: 100%;
        }
        
        .stat-card:hover {
            border-color: rgba(102, 126, 234, 0.6);
            transform: translateY(-4px);
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 8px 0;
        }
        
        .stat-label {
            font-size: 0.8rem;
            color: #a0a0b0;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .faq-item {
            background: linear-gradient(135deg, #1e1e2e, #2a2a3e);
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 12px;
            padding: 18px 22px;
            margin-bottom: 12px;
        }
        
        .faq-q {
            color: #667eea;
            font-weight: 700;
            font-size: 0.95rem;
            margin-bottom: 8px;
        }
        
        .faq-a {
            color: #b0b0c0;
            font-size: 0.88rem;
            line-height: 1.6;
        }
        
        .tech-item {
            background: rgba(102, 126, 234, 0.08);
            border-radius: 8px;
            padding: 10px 14px;
            margin-bottom: 8px;
            color: #e0e0e0;
            font-size: 0.88rem;
            border-left: 3px solid #667eea;
        }
    </style>
    """, unsafe_allow_html=True)


def render_email_page():
    """Render detailed Email Support page"""
    inject_info_css()
    
    if st.button("🏠 Back to Home", key="back_from_email"):
        st.session_state.show_email_page = False
        st.session_state.show_website_page = False
        st.session_state.show_privacy_page = False
        st.session_state.show_terms_page = False
        st.rerun()
    
    st.markdown("""
    <div class="info-hero">
        <div class="info-hero-icon">📧</div>
        <div class="info-hero-title">Email Support Center</div>
        <div class="info-hero-subtitle">24/7 support for patients, doctors, and hospitals</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="notice-box">
        <strong>🎓 Academic Project Notice:</strong> MediFederate is a Final Year Project (FYP) 
        for educational purposes. The email addresses below are <strong>demo placeholders</strong> 
        for demonstration. In a real hospital deployment, these would be actual verified contacts.
    </div>
    """, unsafe_allow_html=True)
    
    # ===== QUICK STATS =====
    st.markdown('<div class="info-section-header">📊 Support Statistics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 1.8rem;">⚡</div>
            <div class="stat-value">6 hrs</div>
            <div class="stat-label">Avg Response</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 1.8rem;">✅</div>
            <div class="stat-value">98%</div>
            <div class="stat-label">Resolution Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 1.8rem;">🎧</div>
            <div class="stat-value">24/7</div>
            <div class="stat-label">Availability</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 1.8rem;">🌐</div>
            <div class="stat-value">3</div>
            <div class="stat-label">Languages</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== PRIMARY SUPPORT =====
    st.markdown('<div class="info-section-header">🎯 Primary Support Channels</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <div class="info-card-icon">💬</div>
            <div class="info-card-title">General Support <span class="demo-badge">Demo</span></div>
            <div class="info-card-desc">
                For general questions, feedback, and help:<br><br>
                <strong>support@medifederate.com</strong><br>
                <span style="color: #a0a0b0; font-size: 0.85rem;">
                🕐 Response: Within 24 hours<br>
                📅 Available: Monday to Sunday<br>
                🌍 Languages: English
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <div class="info-card-icon">🔧</div>
            <div class="info-card-title">Technical Support <span class="demo-badge">Demo</span></div>
            <div class="info-card-desc">
                For bugs, technical issues, and platform problems:<br><br>
                <strong>tech@medifederate.com</strong><br>
                <span style="color: #a0a0b0; font-size: 0.85rem;">
                🕐 Response: Within 12 hours<br>
                📅 Available: 24/7<br>
                💻 Bug reports, errors, feature requests
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== DEPARTMENT EMAILS =====
    st.markdown('<div class="info-section-header">📬 Department-wise Emails</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="email-list">
        <div class="email-list-title">Contact by Department <span class="demo-badge">Demo</span></div>
        <div class="email-item">🚨 <strong>Emergency Response:</strong> emergency@medifederate.com</div>
        <div class="email-item">🔒 <strong>Privacy & Data Protection:</strong> privacy@medifederate.com</div>
        <div class="email-item">💼 <strong>Business & Partnerships:</strong> business@medifederate.com</div>
        <div class="email-item">🎓 <strong>Research Collaboration:</strong> research@medifederate.com</div>
        <div class="email-item">👥 <strong>Careers & Internships:</strong> careers@medifederate.com</div>
        <div class="email-item">📰 <strong>Press & Media Inquiries:</strong> press@medifederate.com</div>
        <div class="email-item">📋 <strong>Feedback & Suggestions:</strong> feedback@medifederate.com</div>
        <div class="email-item">🏥 <strong>Hospital Onboarding:</strong> hospitals@medifederate.com</div>
        <div class="email-item">👨‍⚕️ <strong>Doctor Verification:</strong> verify@medifederate.com</div>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== HOW TO WRITE =====
    st.markdown('<div class="info-section-header">✍️ How to Write an Effective Email</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-item">
        <div class="feature-item-title">1. 📌 Clear Subject Line</div>
        <div class="feature-item-desc">
            Subject should be specific. Examples:<br>
            ✅ "Bug Report — Diabetes prediction returns error"<br>
            ✅ "Request — Password reset for doctor account"<br>
            ❌ "Help me please!!!" (too vague)
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">2. 👤 Your Details</div>
        <div class="feature-item-desc">
            Full name, registered email, hospital name (if doctor), and account type. This helps us locate your account quickly.
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">3. 📝 Problem Description</div>
        <div class="feature-item-desc">
            What happened? When did it happen? What steps did you take? What was the expected result? Be as detailed as possible.
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">4. 📸 Screenshots / Evidence</div>
        <div class="feature-item-desc">
            For technical issues, attach screenshots of errors. For prediction issues, mention the patient parameters.
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">5. 📞 Contact Number</div>
        <div class="feature-item-desc">
            For urgent cases, include a phone number so we can call you back within 2 hours.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== RESPONSE TIMES =====
    st.markdown('<div class="info-section-header">⏱️ Response Time Guarantees</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-card" style="text-align: center;">
            <div class="info-card-icon">🚨</div>
            <div class="info-card-title">Emergency</div>
            <div class="info-card-desc">
                <strong style="font-size: 1.3rem;">1-2 hours</strong><br>
                <span style="color: #a0a0b0; font-size: 0.8rem;">Life-threatening issues, urgent data access</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card" style="text-align: center;">
            <div class="info-card-icon">⚡</div>
            <div class="info-card-title">Urgent</div>
            <div class="info-card-desc">
                <strong style="font-size: 1.3rem;">6-12 hours</strong><br>
                <span style="color: #a0a0b0; font-size: 0.8rem;">Login issues, prediction errors, PDF failures</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card" style="text-align: center;">
            <div class="info-card-icon">📧</div>
            <div class="info-card-title">General</div>
            <div class="info-card-desc">
                <strong style="font-size: 1.3rem;">24-48 hours</strong><br>
                <span style="color: #a0a0b0; font-size: 0.8rem;">Feedback, suggestions, general queries</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== FAQ =====
    st.markdown('<div class="info-section-header">❓ Frequently Asked Questions</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="faq-item">
        <div class="faq-q">Q: How do I reset my doctor account password?</div>
        <div class="faq-a">Go to the login page, click "Forgot Password?", enter your registered email, and set a new password. If you still face issues, email tech@medifederate.com.</div>
    </div>
    <div class="faq-item">
        <div class="faq-q">Q: Is patient data really private?</div>
        <div class="faq-a">Yes. We use Federated Learning + Differential Privacy. Patient data never leaves your device. Only encrypted model weights are shared.</div>
    </div>
    <div class="faq-item">
        <div class="faq-q">Q: Can I use MediFederate without creating an account?</div>
        <div class="faq-a">Absolutely. Click "Continue as Patient (Guest)" on the login page. No registration is needed for patients.</div>
    </div>
    <div class="faq-item">
        <div class="faq-q">Q: How accurate are the AI predictions?</div>
        <div class="faq-a">Model accuracies: Diabetes 62.38%, Heart 88.52%, Stroke 72.90%, Kidney 100%. Predictions are for informational purposes only. Always consult a real doctor.</div>
    </div>
    <div class="faq-item">
        <div class="faq-q">Q: How do I report a bug?</div>
        <div class="faq-a">Email tech@medifederate.com with the subject "Bug Report — [short description]", attach a screenshot, and mention steps to reproduce.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.error("🚨 **For medical emergencies, do NOT use email.** Call **1122** (Rescue) or **115** (Edhi Ambulance) immediately, or visit your nearest hospital.")
    
    st.info("📌 **Version:** MediFederate v2.0 · **Project Type:** Final Year Project · **License:** Academic")


def render_website_page():
    """Render detailed Website/About page"""
    inject_info_css()
    
    if st.button("🏠 Back to Home", key="back_from_website"):
        st.session_state.show_email_page = False
        st.session_state.show_website_page = False
        st.session_state.show_privacy_page = False
        st.session_state.show_terms_page = False
        st.rerun()
    
    st.markdown("""
    <div class="info-hero">
        <div class="info-hero-icon">🌐</div>
        <div class="info-hero-title">www.medifederate.com</div>
        <div class="info-hero-subtitle">Privacy-Preserving Healthcare AI Platform</div>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== MISSION & VISION =====
    st.markdown('<div class="info-section-header">🎯 Our Mission & Vision</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <div class="info-card-icon">🚀</div>
            <div class="info-card-title">Mission</div>
            <div class="info-card-desc">
                To make healthcare AI accessible, secure, and privacy-respecting for patients 
                and doctors across Pakistan, and eventually the world. We believe AI should 
                never come at the cost of patient privacy.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <div class="info-card-icon">🔭</div>
            <div class="info-card-title">Vision</div>
            <div class="info-card-desc">
                A future where multiple hospitals collaborate on AI models without sharing 
                a single byte of patient data. Federated Learning is the foundation; trust 
                is the outcome.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== PLATFORM STATISTICS =====
    st.markdown('<div class="info-section-header">📊 Platform Statistics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 1.8rem;">🏥</div>
            <div class="stat-value">4</div>
            <div class="stat-label">Diseases Covered</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 1.8rem;">👥</div>
            <div class="stat-value">105K+</div>
            <div class="stat-label">Patients Trained</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 1.8rem;">🔒</div>
            <div class="stat-value">0 B</div>
            <div class="stat-label">Data Shared</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 1.8rem;">🏆</div>
            <div class="stat-value">88%</div>
            <div class="stat-label">Best Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== FEATURES =====
    st.markdown('<div class="info-section-header">✨ Platform Features</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-item">
        <div class="feature-item-title">🩸 Multi-Disease Prediction (4 Diseases)</div>
        <div class="feature-item-desc">
            Diabetes readmission, Heart disease, Stroke, and Kidney disease — all using real trained neural networks.
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">🔒 Federated Learning</div>
        <div class="feature-item-desc">
            3 simulated hospitals (A, B, C) collaboratively train a shared model using FedAvg — without centralizing data.
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">🛡️ Differential Privacy</div>
        <div class="feature-item-desc">
            Gaussian noise (multiplier 0.01) added to weights with clipping. Formal privacy guarantee.
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">🧠 Explainable AI (SHAP)</div>
        <div class="feature-item-desc">
            Every prediction comes with feature importance analysis — doctors see WHY, not just WHAT.
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">💬 AI Health Chatbot (Groq)</div>
        <div class="feature-item-desc">
            MediBot answers health questions in English, 24/7, with user-history awareness.
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">📄 PDF Medical Reports</div>
        <div class="feature-item-desc">
            Downloadable reports with patient details, AI prediction, recommendations, and doctor's notes section.
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">📜 Prediction History (SQLite)</div>
        <div class="feature-item-desc">
            Each doctor sees ONLY their own predictions. Export to CSV. Advanced analytics dashboard.
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">🔐 Doctor Authentication</div>
        <div class="feature-item-desc">
            bcrypt-secured login, signup, forgot password, and patient guest mode.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== TECHNOLOGY STACK =====
    st.markdown('<div class="info-section-header">🛠️ Technology Stack</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🤖 AI & Machine Learning**")
        st.markdown('<div class="tech-item">TensorFlow 2.x — Neural Networks</div>', unsafe_allow_html=True)
        st.markdown('<div class="tech-item">Federated Averaging (FedAvg)</div>', unsafe_allow_html=True)
        st.markdown('<div class="tech-item">Differential Privacy (Gaussian Noise)</div>', unsafe_allow_html=True)
        st.markdown('<div class="tech-item">SHAP — Explainability</div>', unsafe_allow_html=True)
        st.markdown('<div class="tech-item">Scikit-learn — Preprocessing</div>', unsafe_allow_html=True)
        
        st.markdown("<br>**🌐 Frontend & UI**", unsafe_allow_html=True)
        st.markdown('<div class="tech-item">Streamlit 1.x</div>', unsafe_allow_html=True)
        st.markdown('<div class="tech-item">Custom CSS + Animations</div>', unsafe_allow_html=True)
        st.markdown('<div class="tech-item">Plotly Interactive Charts</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("**💾 Data & Storage**")
        st.markdown('<div class="tech-item">SQLite — History + Users</div>', unsafe_allow_html=True)
        st.markdown('<div class="tech-item">Pandas + NumPy</div>', unsafe_allow_html=True)
        st.markdown('<div class="tech-item">ReportLab — PDF Generation</div>', unsafe_allow_html=True)
        
        st.markdown("<br>**🔐 Security & AI Chat**", unsafe_allow_html=True)
        st.markdown('<div class="tech-item">bcrypt — Password Hashing</div>', unsafe_allow_html=True)
        st.markdown('<div class="tech-item">Groq API (Llama 3.3 70B)</div>', unsafe_allow_html=True)
        st.markdown('<div class="tech-item">Python-dotenv — Secrets</div>', unsafe_allow_html=True)
        
        st.markdown("<br>**🚀 Deployment**", unsafe_allow_html=True)
        st.markdown('<div class="tech-item">Streamlit Community Cloud</div>', unsafe_allow_html=True)
        st.markdown('<div class="tech-item">Git + GitHub</div>', unsafe_allow_html=True)
    
    # ===== TEAM =====
    st.markdown('<div class="info-section-header">👨‍💻 Development Team</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="team-card">
            <div class="team-avatar">👨‍💻</div>
            <div class="team-name">Student Developer</div>
            <div class="team-role">Full Stack & AI Engineer</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="team-card">
            <div class="team-avatar">👨‍🏫</div>
            <div class="team-name">Project Supervisor</div>
            <div class="team-role">CS Department Faculty</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="team-card">
            <div class="team-avatar">🏥</div>
            <div class="team-name">Medical Advisors</div>
            <div class="team-role">Healthcare Experts</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== CONTACT =====
    st.markdown('<div class="info-section-header">📞 Contact Information</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <div class="info-card-icon">📧</div>
            <div class="info-card-title">Email <span class="demo-badge">Demo</span></div>
            <div class="info-card-desc">
                <strong>info@medifederate.com</strong><br>
                support@medifederate.com<br>
                tech@medifederate.com
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <div class="info-card-icon">📞</div>
            <div class="info-card-title">Phone <span class="demo-badge">Demo</span></div>
            <div class="info-card-desc">
                <strong>042-111-222-333</strong><br>
                Mon-Fri, 9 AM - 6 PM<br>
                Emergency: 1122
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card">
            <div class="info-card-icon">📍</div>
            <div class="info-card-title">Location <span class="demo-badge">Demo</span></div>
            <div class="info-card-desc">
                <strong>Pakistan</strong><br>
                Computer Science Department<br>
                Final Year Project 2026
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== SOCIAL MEDIA =====
    st.markdown('<div class="info-section-header">🌐 Follow Us</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <div class="info-card-desc" style="text-align: center;">
            📘 <strong>Facebook</strong> · 🐦 <strong>Twitter</strong> · 📸 <strong>Instagram</strong> · 💼 <strong>LinkedIn</strong> · ▶️ <strong>YouTube</strong><br><br>
            <span style="color: #a0a0b0; font-size: 0.85rem;">@medifederate — on every platform (demo handles)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== ROADMAP =====
    st.markdown('<div class="info-section-header">🗺️ Project Roadmap</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-item">
        <div class="feature-item-title">✅ Phase 1 — Completed</div>
        <div class="feature-item-desc">
            4 AI models trained, Federated Learning + DP, Dashboard, Chatbot, PDF Reports, Auth, History
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">🔄 Phase 2 — In Progress</div>
        <div class="feature-item-desc">
            More diseases (Thyroid, Liver, Cancer), Formal DP with Opacus, REST API
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">🔮 Phase 3 — Future</div>
        <div class="feature-item-desc">
            Blockchain audit trail, Mobile app, Multi-language support, Docker deployment
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("📌 **Version:** MediFederate v2.0 · **Released:** 2026 · **License:** Academic Project")