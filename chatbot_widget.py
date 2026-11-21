"""
MediBot Floating Widget
Floating button on right side - opens a dialog with 2 tabs:
1. Chat (AI Health Assistant) with typing animation
2. Explainable AI (SHAP Analysis)
"""

import streamlit as st
import pandas as pd
import os
from chatbot import HealthChatbot


def inject_floating_button_css():
    """CSS for floating chat button and typing animation"""
    st.markdown("""
    <style>
        /* Floating Chat Button */
        .st-key-floating_chat_btn {
            position: fixed !important;
            bottom: 25px !important;
            right: 25px !important;
            z-index: 999999 !important;
        }
        
        .st-key-floating_chat_btn button {
            width: 65px !important;
            height: 65px !important;
            border-radius: 50% !important;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            font-size: 28px !important;
            border: none !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
            transition: all 0.3s ease !important;
            padding: 0 !important;
            cursor: pointer !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        
        .st-key-floating_chat_btn button:hover {
            transform: scale(1.1) !important;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.7) !important;
        }
        
        /* Typing animation for welcome message */
        @keyframes typing {
            from { width: 0; }
            to { width: 100%; }
        }
        
        @keyframes blink {
            50% { border-color: transparent; }
        }
        
        .typing-text {
            display: inline-block;
            overflow: hidden;
            white-space: nowrap;
            border-right: 2px solid #667eea;
            animation: typing 2.5s steps(40, end), blink 0.75s step-end infinite;
            font-size: 1rem;
            color: #e0e0e0;
        }
        
        .typing-text-2 {
            display: inline-block;
            overflow: hidden;
            white-space: nowrap;
            border-right: 2px solid #667eea;
            animation: typing 3.5s steps(60, end), blink 0.75s step-end infinite;
            font-size: 0.95rem;
            color: #b0b0b0;
            animation-delay: 2.5s;
            animation-fill-mode: both;
        }
        
        .welcome-card {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
            border-left: 4px solid #667eea;
            padding: 16px 20px;
            border-radius: 10px;
            margin-bottom: 15px;
        }
        
        .welcome-title {
            font-size: 1.15rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 8px;
        }
        
        /* ===== CLEAN TABS DESIGN for Dialog ===== */
        div[data-testid="stDialog"] .stTabs [data-baseweb="tab-list"] {
            gap: 6px !important;
            background: rgba(255, 255, 255, 0.03) !important;
            padding: 6px !important;
            border-radius: 12px !important;
            border-bottom: none !important;
        }
        
        div[data-testid="stDialog"] .stTabs [data-baseweb="tab"] {
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
        
        div[data-testid="stDialog"] .stTabs [data-baseweb="tab"]:hover {
            background: rgba(102, 126, 234, 0.12) !important;
            color: #ffffff !important;
        }
        
        div[data-testid="stDialog"] .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: #ffffff !important;
            box-shadow: 0 4px 14px rgba(102, 126, 234, 0.35) !important;
            font-weight: 600 !important;
        }
        
        /* Remove red underline inside dialog */
        div[data-testid="stDialog"] .stTabs [data-baseweb="tab-highlight"] {
            background: transparent !important;
            display: none !important;
        }
        
        div[data-testid="stDialog"] .stTabs [data-baseweb="tab-border"] {
            background: transparent !important;
            display: none !important;
        }
        
        /* Clean buttons inside dialog */
        div[data-testid="stDialog"] .stButton > button {
            border-radius: 10px !important;
            font-weight: 500 !important;
            transition: all 0.25s ease !important;
            border: 1px solid rgba(102, 126, 234, 0.3) !important;
        }
        
        div[data-testid="stDialog"] .stButton > button:hover {
            border-color: rgba(102, 126, 234, 0.7) !important;
            transform: translateY(-1px) !important;
        }
        
        div[data-testid="stDialog"] .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            border: none !important;
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)


def render_chat_tab():
    """Chatbot tab content with professional welcome"""
    
    # Welcome card with typing animation
    st.markdown("""
    <div class="welcome-card">
        <div class="welcome-title">👋 Hello! I am <strong>MediBot</strong></div>
        <div class="typing-text" style="display:block; border-right:none;">Your AI Health Assistant</div>
        <br>
        <div class="typing-text-2" style="display:block; border-right:none;">I can help you with health-related questions.</div>
    </div>
    """, unsafe_allow_html=True)

    # Chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'chatbot_instance' not in st.session_state:
        st.session_state.chatbot_instance = HealthChatbot()

    # Topic hints
    st.markdown("**Available Topics:** 🩸 Diabetes · ❤️ Heart · 🧠 Stroke · ⚖️ BMI · 💓 BP · 🍎 Diet · 🏃 Exercise · 🚨 Emergency")

    st.markdown("---")

    # Quick question buttons
    st.markdown("**💡 Quick Questions:**")
    col1, col2, col3, col4 = st.columns(4)

    clicked_query = None
    with col1:
        if st.button("🩸 Sugar", key="wq1", use_container_width=True):
            clicked_query = "My sugar level is 200, what should I do?"
    with col2:
        if st.button("⚖️ BMI", key="wq2", use_container_width=True):
            clicked_query = "Calculate BMI for 70 kg 170 cm"
    with col3:
        if st.button("💓 BP", key="wq3", use_container_width=True):
            clicked_query = "My blood pressure is high, what should I do?"
    with col4:
        if st.button("🚨 Help", key="wq4", use_container_width=True):
            clicked_query = "What is the emergency number?"

    st.markdown("---")

    # Display chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            with st.chat_message("user"):
                st.markdown(message['content'])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(message['content'])

    # Chat input (at the bottom)
    user_input = st.chat_input("Ask your health question...", key="chat_input_widget")

    if clicked_query:
        user_input = clicked_query

    if user_input:
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })
        bot_response = st.session_state.chatbot_instance.get_response(user_input)
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': bot_response
        })
        st.rerun()

    # Clear chat button
    if len(st.session_state.chat_history) > 0:
        if st.button("🗑️ Clear Chat", key="clear_widget"):
            st.session_state.chat_history = []
            st.rerun()


def render_explainable_ai_tab():
    """Explainable AI (SHAP) tab content"""
    st.markdown("""
    **SHAP (SHapley Additive exPlanations)** explains why the AI made its prediction.
    This is **explainable AI** — it shows both the answer and the reasoning behind it.
    """)

    if os.path.exists('shap_feature_importance.csv'):
        importance_df = pd.read_csv('shap_feature_importance.csv')

        st.subheader("📊 Top 15 Features (Most Important for AI)")
        st.dataframe(importance_df.head(15), use_container_width=True)

        st.subheader("📈 Feature Importance Chart")
        top_10 = importance_df.head(10)
        st.bar_chart(top_10.set_index('Feature')['SHAP Importance'])

        if os.path.exists('shap_summary.png'):
            st.subheader("🖼️ SHAP Summary Plot")
            st.image('shap_summary.png', use_container_width=True)

        st.info("""
        **How to Interpret:**
        - Features listed at the top have the highest impact
        - `number_inpatient` (0.0603) is the most important feature
        - Meaning: If a patient has been admitted multiple times before, 
          the risk of readmission is significantly higher
        """)
    else:
        st.warning("⚠️ SHAP analysis not found. Please run `python shap_explainer.py` first.")


@st.dialog("🤖 MediBot — AI Assistant", width="large")
def show_medibot_dialog():
    """Popup dialog with 2 tabs: Chat + Explainable AI"""
    
    # Inject CSS inside dialog for tabs
    st.markdown("""
    <style>
        /* Clean tabs inside dialog */
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
        
        /* Remove red underline */
        .stTabs [data-baseweb="tab-highlight"] {
            background: transparent !important;
            display: none !important;
        }
        
        .stTabs [data-baseweb="tab-border"] {
            background: transparent !important;
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    chat_tab, xai_tab = st.tabs([
        "💬 Chat",
        "🔍 Explainable AI"
    ])

    with chat_tab:
        render_chat_tab()

    with xai_tab:
        render_explainable_ai_tab()


def render_floating_chatbot():
    """Render floating button on the right side"""
    inject_floating_button_css()

    if st.button("💬", key="floating_chat_btn"):
        show_medibot_dialog()