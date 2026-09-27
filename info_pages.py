"""
MediFederate Info Pages
Email Support and Website detail pages with back navigation
"""

import streamlit as st


def inject_info_css():
    """CSS for info pages"""
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
            padding-top: 4rem;
            padding-bottom: 4rem;
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .info-hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 45px 40px;
            border-radius: 18px;
            color: white;
            margin-bottom: 35px;
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
            position: relative;
            overflow: hidden;
            text-align: center;
        }
        
        .info-hero::before {
            content: "";
            position: absolute;
            top: -50%;
            right: -10%;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            border-radius: 50%;
        }
        
        .info-hero-icon {
            font-size: 3.5rem;
            margin-bottom: 12px;
            position: relative;
            z-index: 2;
        }
        
        .info-hero-title {
            font-size: 2.2rem;
            font-weight: 800;
            margin: 0;
            letter-spacing: -0.5px;
            position: relative;
            z-index: 2;
        }
        
        .info-hero-subtitle {
            font-size: 1rem;
            font-weight: 400;
            opacity: 0.95;
            margin-top: 10px;
            position: relative;
            z-index: 2;
        }
        
        .info-card {
            background: linear-gradient(135deg, #1e1e2e 0%, #2a2a3e 100%);
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 14px;
            padding: 22px;
            margin-bottom: 18px;
            transition: all 0.3s ease;
        }
        
        .info-card:hover {
            border-color: rgba(102, 126, 234, 0.6);
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        }
        
        .info-card-icon {
            font-size: 2rem;
            margin-bottom: 10px;
        }
        
        .info-card-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 6px;
        }
        
        .info-card-desc {
            font-size: 0.9rem;
            color: #b0b0c0;
            line-height: 1.6;
        }
        
        .info-card-desc strong {
            color: #10b981;
        }
        
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
            padding: 6px 0;
            border-bottom: 1px dashed rgba(102, 126, 234, 0.15);
        }
        
        .email-item:last-child {
            border-bottom: none;
        }
        
        .email-item strong {
            color: #10b981;
            font-weight: 600;
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
        
        .feature-item-title {
            color: #ffffff;
            font-weight: 600;
            font-size: 0.95rem;
            margin-bottom: 4px;
        }
        
        .feature-item-desc {
            color: #a0a0b0;
            font-size: 0.85rem;
            line-height: 1.5;
        }
        
        .team-card {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .team-card:hover {
            transform: translateY(-4px);
            border-color: rgba(102, 126, 234, 0.6);
        }
        
        .team-avatar {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .team-name {
            color: #ffffff;
            font-weight: 700;
            font-size: 1rem;
            margin-bottom: 4px;
        }
        
        .team-role {
            color: #667eea;
            font-size: 0.8rem;
            font-weight: 500;
        }
    </style>
    """, unsafe_allow_html=True)


def render_email_page():
    """Render Email Support detail page"""
    inject_info_css()
    
    if st.button("🏠 Back to Home", key="back_from_info"):
        st.session_state.show_email_page = False
        st.session_state.show_website_page = False
        st.rerun()
    
    st.markdown("""
    <div class="info-hero">
        <div class="info-hero-icon">📧</div>
        <div class="info-hero-title">Email Support</div>
        <div class="info-hero-subtitle">We're here to help — reach out to us anytime</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="info-section-header">🎯 Primary Support</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <div class="info-card-icon">💬</div>
            <div class="info-card-title">General Support</div>
            <div class="info-card-desc">
                For general questions, feedback, and help:<br><br>
                <strong>support@medifederate.com</strong><br>
                <span style="color: #a0a0b0; font-size: 0.85rem;">Response: Within 24 hours</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <div class="info-card-icon">🔧</div>
            <div class="info-card-title">Technical Support</div>
            <div class="info-card-desc">
                For bugs, technical issues, and platform problems:<br><br>
                <strong>tech@medifederate.com</strong><br>
                <span style="color: #a0a0b0; font-size: 0.85rem;">Response: Within 12 hours</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="info-section-header">📬 Department-wise Emails</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="email-list">
        <div class="email-list-title">Department Contact</div>
        <div class="email-item">🚨 <strong>Emergency:</strong> emergency@medifederate.com</div>
        <div class="email-item">🔒 <strong>Privacy & Data:</strong> privacy@medifederate.com</div>
        <div class="email-item">💼 <strong>Business & Partnerships:</strong> business@medifederate.com</div>
        <div class="email-item">🎓 <strong>Research Collaboration:</strong> research@medifederate.com</div>
        <div class="email-item">👥 <strong>Careers & Jobs:</strong> careers@medifederate.com</div>
        <div class="email-item">📰 <strong>Press & Media:</strong> press@medifederate.com</div>
        <div class="email-item">📋 <strong>Feedback & Suggestions:</strong> feedback@medifederate.com</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="info-section-header">✍️ How to Write an Effective Email</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-item">
        <div class="feature-item-title">1. Clear Subject Line</div>
        <div class="feature-item-desc">Example: "Bug Report — Diabetes prediction error" or "Request — Password reset"</div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">2. Your Details</div>
        <div class="feature-item-desc">Full name, registered email, and (if doctor) hospital name — please include</div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">3. Problem/Question Detail</div>
        <div class="feature-item-desc">What is the issue, when it happened, and what steps you took — describe in detail</div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">4. Screenshots (if applicable)</div>
        <div class="feature-item-desc">For technical issues, attach screenshots of the error</div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">5. Contact Number</div>
        <div class="feature-item-desc">For urgent cases, include your phone number</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="info-section-header">⏱️ Response Times</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-card" style="text-align: center;">
            <div class="info-card-icon">🚨</div>
            <div class="info-card-title">Emergency</div>
            <div class="info-card-desc"><strong>1-2 hours</strong></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card" style="text-align: center;">
            <div class="info-card-icon">⚡</div>
            <div class="info-card-title">Urgent</div>
            <div class="info-card-desc"><strong>6-12 hours</strong></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card" style="text-align: center;">
            <div class="info-card-icon">📧</div>
            <div class="info-card-title">General</div>
            <div class="info-card-desc"><strong>24-48 hours</strong></div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.error("🚨 **For medical emergencies, do NOT use email.** Please call **1122** (Rescue) or visit your nearest hospital immediately.")


def render_website_page():
    """Render Website/About detail page"""
    inject_info_css()
    
    if st.button("🏠 Back to Home", key="back_from_info"):
        st.session_state.show_email_page = False
        st.session_state.show_website_page = False
        st.rerun()
    
    st.markdown("""
    <div class="info-hero">
        <div class="info-hero-icon">🌐</div>
        <div class="info-hero-title">www.medifederate.com</div>
        <div class="info-hero-subtitle">Privacy-Preserving Healthcare AI Platform</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="info-section-header">🏥 About MediFederate</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <div class="info-card-desc">
            <strong>MediFederate</strong> is a privacy-preserving healthcare AI platform that uses 
            <strong>Federated Learning</strong> and <strong>Differential Privacy</strong> to enable 
            multiple hospitals to train AI models together — <strong>without sharing any patient data.</strong>
            <br><br>
            Our mission: <em>Make healthcare AI accessible, secure, and privacy-respecting</em> 
            — for Pakistan and the world.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="info-section-header">✨ Platform Features</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-item">
        <div class="feature-item-title">🩸 Multi-Disease Prediction</div>
        <div class="feature-item-desc">Diabetes, Heart Disease, and Stroke — AI prediction for three major diseases</div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">🔒 Privacy Guaranteed</div>
        <div class="feature-item-desc">Patient data never leaves the hospital — only encrypted model weights are shared</div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">🧠 Explainable AI (SHAP)</div>
        <div class="feature-item-desc">Every prediction comes with reasoning — critical for medical trust</div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">💬 AI Health Chatbot</div>
        <div class="feature-item-desc">MediBot available 24/7 — answers health questions in English and Roman Urdu</div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">📄 PDF Medical Reports</div>
        <div class="feature-item-desc">Downloadable medical report for every prediction — share with your doctor</div>
    </div>
    <div class="feature-item">
        <div class="feature-item-title">📜 Prediction History</div>
        <div class="feature-item-desc">Doctors can track all their predictions — stored in SQLite database</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="info-section-header">🛠️ Technology Stack</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <div class="info-card-icon">🤖</div>
            <div class="info-card-title">Federated Learning</div>
            <div class="info-card-desc">3 hospitals collaborative training with FedAvg algorithm — <strong>Zero data centralization</strong></div>
        </div>
        <div class="info-card">
            <div class="info-card-icon">🔒</div>
            <div class="info-card-title">Differential Privacy</div>
            <div class="info-card-desc">Gaussian noise addition with weight clipping — <strong>(ε, δ) privacy guarantee</strong></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <div class="info-card-icon">🧠</div>
            <div class="info-card-title">Deep Learning</div>
            <div class="info-card-desc">TensorFlow-based neural networks — <strong>62-88% accuracy</strong></div>
        </div>
        <div class="info-card">
            <div class="info-card-icon">💬</div>
            <div class="info-card-title">Groq AI Chatbot</div>
            <div class="info-card-desc">Llama 3.3 70B powered — <strong>Real-time bilingual responses</strong></div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="info-section-header">👨‍💻 Development Team</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="team-card">
            <div class="team-avatar">👨‍💻</div>
            <div class="team-name">Student Developer</div>
            <div class="team-role">Full Stack & AI</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="team-card">
            <div class="team-avatar">👨‍🏫</div>
            <div class="team-name">Project Supervisor</div>
            <div class="team-role">CS Department</div>
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
    
    st.markdown('<div class="info-section-header">📞 Contact Us</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <div class="info-card-icon">📧</div>
            <div class="info-card-title">Email</div>
            <div class="info-card-desc">
                <strong>info@medifederate.com</strong><br>
                support@medifederate.com
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <div class="info-card-icon">📞</div>
            <div class="info-card-title">Phone</div>
            <div class="info-card-desc">
                <strong>042-111-222-333</strong><br>
                Mon-Fri, 9 AM - 6 PM
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="info-section-header">🌐 Follow Us</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <div class="info-card-desc" style="text-align: center;">
            📘 Facebook · 🐦 Twitter · 📸 Instagram · 💼 LinkedIn · ▶️ YouTube<br><br>
            <span style="color: #a0a0b0; font-size: 0.85rem;">@medifederate — on every platform</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("📌 **Version:** MediFederate v2.0 · **Released:** 2026 · **License:** Academic Project")