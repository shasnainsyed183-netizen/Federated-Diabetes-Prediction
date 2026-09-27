"""
MediBot Full-Page Chat Interface
ChatGPT-style layout with sidebar history
Bilingual support (English + Roman Urdu)
"""

import streamlit as st
from datetime import datetime
import uuid
from chatbot import HealthChatbot


def init_chat_state():
    """Initialize chat sessions"""
    if 'chat_sessions' not in st.session_state:
        st.session_state.chat_sessions = {}
    if 'current_chat_id' not in st.session_state:
        _create_new_chat()
    if 'chatbot_instance' not in st.session_state:
        st.session_state.chatbot_instance = HealthChatbot()


def _create_new_chat():
    """Create a new chat session"""
    new_id = str(uuid.uuid4())[:8]
    st.session_state.chat_sessions[new_id] = {
        'title': 'New Chat',
        'created_at': datetime.now().strftime('%b %d, %H:%M'),
        'messages': []
    }
    st.session_state.current_chat_id = new_id


def _delete_chat(chat_id):
    """Delete a chat session"""
    if chat_id in st.session_state.chat_sessions:
        del st.session_state.chat_sessions[chat_id]
        if st.session_state.current_chat_id == chat_id:
            if st.session_state.chat_sessions:
                st.session_state.current_chat_id = list(st.session_state.chat_sessions.keys())[-1]
            else:
                _create_new_chat()


def inject_chat_page_css():
    """Custom CSS - hide avatars, add floating back button"""
    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        .main .block-container {
            padding-top: 4rem;
            padding-bottom: 6rem;
            max-width: 900px;
            margin: 0 auto;
        }
        
        /* ===== HIDE AVATARS ===== */
        [data-testid="stChatMessageAvatarUser"],
        [data-testid="stChatMessageAvatarAssistant"] {
            display: none !important;
        }
        
        /* Chat message styling */
        [data-testid="stChatMessage"] {
            background: rgba(255, 255, 255, 0.03) !important;
            border-radius: 12px !important;
            padding: 14px 18px !important;
            margin-bottom: 12px !important;
            border: 1px solid rgba(102, 126, 234, 0.1) !important;
        }
        
        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
            background: rgba(102, 126, 234, 0.08) !important;
            border-color: rgba(102, 126, 234, 0.25) !important;
        }
        
        [data-testid="stChatMessageContent"] {
            width: 100% !important;
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
        }
        
        /* Chat input */
        [data-testid="stChatInput"] {
            border-radius: 14px !important;
            border: 1px solid rgba(102, 126, 234, 0.3) !important;
        }
        
        [data-testid="stChatInput"]:focus-within {
            border-color: rgba(102, 126, 234, 0.8) !important;
        }
        
        /* Buttons */
        .stButton > button {
            border-radius: 10px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
        }
        
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
        }
        
        /* Chat header */
        .chat-header {
            text-align: center;
            padding: 20px 0;
        }
        
        .chat-title {
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
        }
        
        .chat-subtitle {
            color: #808090;
            font-size: 0.9rem;
        }
        
        /* ===== FLOATING BACK BUTTON (TOP-LEFT) ===== */
        .st-key-floating_back_btn {
            position: fixed !important;
            top: 15px !important;
            left: 15px !important;
            z-index: 999999 !important;
        }
        
        .st-key-floating_back_btn button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 8px 20px !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            box-shadow: 0 4px 14px rgba(102, 126, 234, 0.5) !important;
            transition: all 0.25s ease !important;
            height: auto !important;
            width: auto !important;
        }
        
        .st-key-floating_back_btn button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.7) !important;
        }
    </style>
    """, unsafe_allow_html=True)


def render_chat_page():
    """Render the full ChatGPT-style chat page"""
    init_chat_state()
    inject_chat_page_css()
    
    # ===== FLOATING BACK BUTTON (TOP-LEFT) =====
    if st.button("🏠 Back to Home", key="floating_back_btn"):
        st.session_state.show_chat_page = False
        st.rerun()
    
    # ============ SIDEBAR ============
    with st.sidebar:
        # ===== BACK BUTTON (TOP OF SIDEBAR) =====
        if st.button("🏠  Back to Home", use_container_width=True, type="primary", key="back_home_sidebar"):
            st.session_state.show_chat_page = False
            st.rerun()
        
        st.markdown("---")
        
        st.markdown("""
        <div style="text-align:center; padding: 8px 0 16px 0;">
            <div style="font-size: 2rem;">🤖</div>
            <h3 style="color: white; margin: 4px 0;">MediBot</h3>
            <p style="color: #808090; font-size: 0.75rem; margin: 0;">AI Health Assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("➕  New Chat", use_container_width=True):
            _create_new_chat()
            st.rerun()
        
        st.markdown("---")
        st.markdown("##### 💬 Chat History")
        
        # List all chats (newest first)
        chat_items = list(st.session_state.chat_sessions.items())[::-1]
        
        for chat_id, chat_data in chat_items:
            is_active = chat_id == st.session_state.current_chat_id
            title = chat_data['title']
            
            if len(title) > 28:
                title = title[:28] + "..."
            
            col1, col2 = st.columns([5, 1])
            
            with col1:
                button_label = f"**{title}**" if is_active else title
                if st.button(
                    f"{'🟢 ' if is_active else ''}{button_label}",
                    key=f"chat_item_{chat_id}",
                    use_container_width=True
                ):
                    st.session_state.current_chat_id = chat_id
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"del_{chat_id}", help="Delete"):
                    _delete_chat(chat_id)
                    st.rerun()
        
        st.markdown("---")
        
        if st.button("🗑️  Clear All Chats", use_container_width=True):
            st.session_state.chat_sessions = {}
            _create_new_chat()
            st.rerun()
    
    # ============ MAIN CHAT ============
    current_chat = st.session_state.chat_sessions[st.session_state.current_chat_id]
    
    st.markdown(f"""
    <div class="chat-header">
        <div class="chat-title">🤖 MediBot</div>
        <div class="chat-subtitle">{current_chat['created_at']} · English & Roman Urdu</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ============ WELCOME SCREEN ============
    if not current_chat['messages']:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h2 style="color: #ffffff;">How can I help you today?</h2>
            <p style="color: #808090;">
                Ask in English or Roman Urdu
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("**🌡️ Common Symptoms:**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🌡️ I have fever", use_container_width=True):
                _handle_message("I have fever")
        with col2:
            if st.button("🤕 I have headache", use_container_width=True):
                _handle_message("I have headache")
        with col3:
            if st.button("🤧 I have cold & cough", use_container_width=True):
                _handle_message("I have cold and cough")
        
        col4, col5, col6 = st.columns(3)
        with col4:
            if st.button("🤢 Stomach pain", use_container_width=True):
                _handle_message("I have stomach pain")
        with col5:
            if st.button("💧 I have diarrhea", use_container_width=True):
                _handle_message("I have diarrhea")
        with col6:
            if st.button("🩹 I have allergy", use_container_width=True):
                _handle_message("I have allergy")
        
        st.markdown("---")
        st.markdown("**🩺 Chronic Conditions:**")
        
        col7, col8, col9 = st.columns(3)
        with col7:
            if st.button("🩸 Diabetes / Sugar", use_container_width=True):
                _handle_message("I have diabetes, what should I do?")
        with col8:
            if st.button("💓 BP High", use_container_width=True):
                _handle_message("My blood pressure is high")
        with col9:
            if st.button("🧠 Stroke Info", use_container_width=True):
                _handle_message("Tell me about stroke")
        
        st.markdown("---")
        st.markdown("**🇵🇰 Roman Urdu Suggestions:**")
        
        col10, col11 = st.columns(2)
        with col10:
            if st.button("🌡️ Mujhe bukhar hai", use_container_width=True):
                _handle_message("Mujhe bukhar hai kya karoon?")
        with col11:
            if st.button("🤕 Sar dard ho raha hai", use_container_width=True):
                _handle_message("Sar dard ho raha hai kya karoon?")
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #808090; font-size: 0.85rem; padding: 20px 0;">
            <strong>Topics I can help with:</strong><br><br>
            🌡️ Fever · 🤕 Headache · 🤧 Cold/Cough · 🤢 Stomach · 💧 Diarrhea · 🩹 Allergy · 🩸 Diabetes · ❤️ Heart · 🧠 Stroke · ⚖️ BMI · 💓 BP · 🍎 Diet · 🏃 Exercise · 🚨 Emergency
        </div>
        """, unsafe_allow_html=True)
    
    # ============ DISPLAY MESSAGES ============
    for msg in current_chat['messages']:
        if msg['role'] == 'user':
            with st.chat_message("user"):
                st.markdown(msg['content'])
        else:
            with st.chat_message("assistant"):
                st.markdown(msg['content'])
    
    # ============ CHAT INPUT ============
    user_input = st.chat_input("Message MediBot... (English ya Roman Urdu mein)")
    
    if user_input:
        _handle_message(user_input)


def _handle_message(user_input):
    """Process user message"""
    current_chat = st.session_state.chat_sessions[st.session_state.current_chat_id]
    
    current_chat['messages'].append({
        'role': 'user',
        'content': user_input
    })
    
    if len(current_chat['messages']) == 1:
        title = user_input[:35]
        if len(user_input) > 35:
            title += "..."
        current_chat['title'] = title
    
    bot_response = st.session_state.chatbot_instance.get_response(user_input)
    current_chat['messages'].append({
        'role': 'assistant',
        'content': bot_response
    })
    
    st.rerun()


def inject_floating_button_css():
    """Floating chat button CSS"""
    st.markdown("""
    <style>
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
    </style>
    """, unsafe_allow_html=True)


def render_floating_chatbot():
    """Render floating button"""
    inject_floating_button_css()
    
    if st.button("💬", key="floating_chat_btn"):
        st.session_state.show_chat_page = True
        st.rerun()