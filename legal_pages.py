"""
MediFederate Legal Pages
Privacy Policy and Terms of Service (English only)
"""

import streamlit as st


def inject_legal_css():
    """CSS for legal pages"""
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
            max-width: 900px;
            margin: 0 auto;
        }
        
        .legal-hero {
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 40px;
            border-radius: 18px;
            color: white;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        }
        
        .legal-hero-icon { font-size: 3rem; margin-bottom: 10px; }
        .legal-hero-title { font-size: 2rem; font-weight: 800; margin: 0; }
        .legal-hero-subtitle { font-size: 0.95rem; opacity: 0.9; margin-top: 10px; }
        
        .legal-section {
            background: linear-gradient(135deg, #1e1e2e, #2a2a3e);
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 12px;
            padding: 24px 28px;
            margin-bottom: 18px;
        }
        
        .legal-section h3 {
            color: #667eea;
            font-size: 1.15rem;
            font-weight: 700;
            margin-top: 0;
            margin-bottom: 12px;
        }
        
        .legal-section p, .legal-section li {
            color: #c0c0d0;
            font-size: 0.92rem;
            line-height: 1.7;
            margin-bottom: 8px;
        }
        
        .legal-section ul {
            padding-left: 20px;
        }
        
        .legal-section strong {
            color: #ffffff;
        }
        
        .legal-warning {
            background: rgba(245, 158, 11, 0.1);
            border-left: 4px solid #f59e0b;
            border-radius: 10px;
            padding: 16px 20px;
            margin: 20px 0;
            color: #fcd34d;
            font-size: 0.9rem;
            line-height: 1.6;
        }
        
        .legal-info {
            background: rgba(59, 130, 246, 0.1);
            border-left: 4px solid #3b82f6;
            border-radius: 10px;
            padding: 16px 20px;
            margin: 20px 0;
            color: #93c5fd;
            font-size: 0.9rem;
            line-height: 1.6;
        }
        
        .last-updated {
            text-align: center;
            color: #808090;
            font-size: 0.82rem;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid rgba(102, 126, 234, 0.15);
        }
    </style>
    """, unsafe_allow_html=True)


def render_privacy_policy():
    """Render Privacy Policy page"""
    inject_legal_css()
    
    if st.button("🏠 Back to Home", key="back_from_privacy"):
        st.session_state.show_privacy_page = False
        st.session_state.show_terms_page = False
        st.rerun()
    
    st.markdown("""
    <div class="legal-hero">
        <div class="legal-hero-icon">🔒</div>
        <div class="legal-hero-title">Privacy Policy</div>
        <div class="legal-hero-subtitle">How MediFederate protects your data</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="legal-info">
        <strong>🎓 Academic Project Notice:</strong> MediFederate is a Final Year Project (FYP) 
        developed for educational and research purposes. It is NOT a commercial healthcare 
        service and should not be used for real medical decisions.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="legal-section">
        <h3>1. Our Privacy Commitment</h3>
        <p>
            MediFederate uses <strong>Federated Learning</strong> and <strong>Differential Privacy</strong> 
            to protect patient data. Our core principle is simple: <strong>your data never leaves your device</strong>.
        </p>
        <ul>
            <li>Patient data is processed locally — never uploaded to any server</li>
            <li>Only encrypted model weights are shared between simulated hospitals</li>
            <li>Gaussian noise is added to protect individual patient privacy</li>
            <li>No patient identifiers are stored or transmitted</li>
        </ul>
    </div>
    
    <div class="legal-section">
        <h3>2. What Data We Collect</h3>
        <p><strong>For Patients (Guest Mode):</strong></p>
        <ul>
            <li>No personal information collected</li>
            <li>Predictions are stored with "guest" tag</li>
            <li>Session data is cleared when you close the browser</li>
        </ul>
        <p><strong>For Doctors (Registered):</strong></p>
        <ul>
            <li>Full name and email (for login)</li>
            <li>Password (securely hashed with bcrypt)</li>
            <li>Hospital affiliation (optional)</li>
            <li>Prediction history (for your reference)</li>
        </ul>
    </div>
    
    <div class="legal-section">
        <h3>3. How We Use Your Data</h3>
        <ul>
            <li><strong>Patient predictions:</strong> Used only for AI model inference and history tracking</li>
            <li><strong>Doctor accounts:</strong> Used only for authentication and access control</li>
            <li><strong>Chatbot conversations:</strong> Sent to Groq API for processing (not stored permanently)</li>
            <li><strong>PDF reports:</strong> Generated locally, never uploaded anywhere</li>
        </ul>
    </div>
    
    <div class="legal-section">
        <h3>4. Data Retention</h3>
        <ul>
            <li>Chat sessions: Cleared on browser close</li>
            <li>Prediction history: Stored locally in SQLite database</li>
            <li>User accounts: Stored until you delete them</li>
            <li>No data is retained on external servers</li>
        </ul>
    </div>
    
    <div class="legal-section">
        <h3>5. Federated Learning & Differential Privacy</h3>
        <p>
            This platform demonstrates <strong>Federated Learning</strong> — a technique where 
            multiple hospitals train AI models together without sharing patient data.
        </p>
        <ul>
            <li><strong>Federated Averaging (FedAvg):</strong> Only model weights are averaged, not data</li>
            <li><strong>Differential Privacy:</strong> Gaussian noise (multiplier 0.01) added to weights</li>
            <li><strong>Result:</strong> Accurate AI models with complete patient privacy</li>
        </ul>
    </div>
    
    <div class="legal-section">
        <h3>6. Third-Party Services</h3>
        <ul>
            <li><strong>Groq API:</strong> Used for AI chatbot (subject to Groq's privacy policy)</li>
            <li><strong>Streamlit Cloud:</strong> Hosting platform (for this academic demo)</li>
            <li><strong>Unsplash:</strong> Gallery images (external CDN)</li>
        </ul>
    </div>
    
    <div class="legal-section">
        <h3>7. Your Rights</h3>
        <ul>
            <li>Right to access your data (History tab)</li>
            <li>Right to delete your data (Clear All button)</li>
            <li>Right to export your data (CSV export)</li>
            <li>Right to use the platform anonymously (Guest Mode)</li>
        </ul>
    </div>
    
    <div class="legal-section">
        <h3>8. Children's Privacy</h3>
        <p>
            MediFederate is not intended for children under 13. We do not knowingly collect 
            data from children. Parents and guardians should supervise any use by minors.
        </p>
    </div>
    
    <div class="legal-section">
        <h3>9. Changes to This Policy</h3>
        <p>
            This policy may be updated as the project evolves. The "Last Updated" date 
            below indicates the most recent revision.
        </p>
    </div>
    
    <div class="legal-section">
        <h3>10. Contact Us</h3>
        <p>For privacy-related questions:</p>
        <ul>
            <li><strong>Email:</strong> privacy@medifederate.com (demo)</li>
            <li><strong>Project Type:</strong> Final Year Project (Academic)</li>
        </ul>
    </div>
    
    <div class="last-updated">
        Last Updated: September 2026 · Version 1.0
    </div>
    """, unsafe_allow_html=True)


def render_terms_of_service():
    """Render Terms of Service page"""
    inject_legal_css()
    
    if st.button("🏠 Back to Home", key="back_from_terms"):
        st.session_state.show_privacy_page = False
        st.session_state.show_terms_page = False
        st.rerun()
    
    st.markdown("""
    <div class="legal-hero">
        <div class="legal-hero-icon">📋</div>
        <div class="legal-hero-title">Terms of Service</div>
        <div class="legal-hero-subtitle">Rules for using MediFederate</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="legal-warning">
        <strong>⚠️ IMPORTANT MEDICAL DISCLAIMER:</strong> MediFederate is an AI system for 
        <strong>educational purposes only</strong>. It is NOT a substitute for professional 
        medical advice, diagnosis, or treatment. Always consult a qualified healthcare 
        provider for medical decisions. <strong>In emergencies, call 1122 immediately.</strong>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="legal-section">
        <h3>1. Acceptance of Terms</h3>
        <p>
            By using MediFederate, you agree to these Terms of Service. If you do not agree, 
            please do not use the platform.
        </p>
    </div>
    
    <div class="legal-section">
        <h3>2. What MediFederate Provides</h3>
        <ul>
            <li><strong>Educational AI Predictions:</strong> Diabetes, Heart, Stroke, Kidney</li>
            <li><strong>AI Health Chatbot:</strong> For general health information (Groq-powered)</li>
            <li><strong>PDF Reports:</strong> Downloadable medical reports</li>
            <li><strong>Medical Gallery:</strong> General health knowledge</li>
            <li><strong>Contacts Directory:</strong> Emergency and hospital numbers</li>
        </ul>
    </div>
    
    <div class="legal-section">
        <h3>3. What MediFederate Does NOT Provide</h3>
        <ul>
            <li>Professional medical diagnosis</li>
            <li>Prescription or treatment advice</li>
            <li>Real-time medical emergency services</li>
            <li>Replacement for a qualified doctor</li>
            <li>Legal or financial medical advice</li>
        </ul>
    </div>
    
    <div class="legal-section">
        <h3>4. User Responsibilities</h3>
        <p>As a user of MediFederate, you agree to:</p>
        <ul>
            <li>Use the platform only for educational purposes</li>
            <li>Never rely solely on AI predictions for medical decisions</li>
            <li>Always consult a real doctor for health concerns</li>
            <li>Provide accurate information when using the platform</li>
            <li>Not misuse the platform for any illegal purpose</li>
            <li>Not attempt to hack, scrape, or reverse-engineer the platform</li>
        </ul>
    </div>
    
    <div class="legal-section">
        <h3>5. Medical Disclaimer</h3>
        <p>
            <strong>CRITICAL:</strong> AI predictions may be inaccurate. The models are trained 
            on limited datasets and should not be used for real diagnosis.
        </p>
        <ul>
            <li>Model accuracies: Diabetes 62%, Heart 88%, Stroke 73%, Kidney 100%</li>
            <li>These are <strong>statistical predictions</strong>, not diagnoses</li>
            <li>False positives and false negatives can occur</li>
            <li>Always verify with a qualified healthcare professional</li>
        </ul>
    </div>
    
    <div class="legal-section">
        <h3>6. Limitation of Liability</h3>
        <p>
            MediFederate and its developers are <strong>not liable</strong> for any damages 
            arising from:
        </p>
        <ul>
            <li>Reliance on AI predictions for medical decisions</li>
            <li>Inaccuracies in the AI models</li>
            <li>Data loss or service interruptions</li>
            <li>Third-party services (Groq, Streamlit Cloud, Unsplash)</li>
        </ul>
    </div>
    
    <div class="legal-section">
        <h3>7. Guest Mode</h3>
        <p>
            Patients can use MediFederate without registration (Guest Mode). No personal 
            information is required. Predictions are still logged with a "guest" tag for 
            system statistics but are not linked to any individual.
        </p>
    </div>
    
    <div class="legal-section">
        <h3>8. Doctor Accounts</h3>
        <ul>
            <li>Registration requires a valid email</li>
            <li>Passwords are hashed with bcrypt — we never store plain passwords</li>
            <li>You are responsible for maintaining account security</li>
            <li>Do not share your account credentials with anyone</li>
        </ul>
    </div>
    
    <div class="legal-section">
        <h3>9. Prohibited Actions</h3>
        <p>You may NOT:</p>
        <ul>
            <li>Use the platform for commercial purposes without permission</li>
            <li>Attempt to access other users' data</li>
            <li>Upload malicious code</li>
            <li>Impersonate a doctor or healthcare provider</li>
            <li>Use AI predictions to provide real medical advice</li>
        </ul>
    </div>
    
    <div class="legal-section">
        <h3>10. Changes to Terms</h3>
        <p>
            These terms may be updated periodically. Continued use of the platform 
            constitutes acceptance of updated terms.
        </p>
    </div>
    
    <div class="legal-section">
        <h3>11. Academic Purpose</h3>
        <p>
            MediFederate is a <strong>Final Year Project (FYP)</strong> submitted as part of 
            a Computer Science degree. It is not a commercial product and should not be 
            treated as such.
        </p>
    </div>
    
    <div class="last-updated">
        Last Updated: September 2026 · Version 1.0
    </div>
    """, unsafe_allow_html=True)