"""
MediBot Full-Page Chat Interface
ChatGPT-style layout with persistent sidebar history (SQLite)
English only
"""

import streamlit as st
from datetime import datetime
from chatbot import HealthChatbot
import chat_history_db as chat_db


def _get_current_user_email():
    """Get current user's email from session state"""
    user = st.session_state.get('user', {})
    return user.get('email', 'guest@medifederate')


def init_chat_state():
    """Initialize chat session state (loads from DB)"""
    user_email = _get_current_user_email()
    
    if 'chat_sessions' not in st.session_state:
        chats = chat_db.get_user_chats(user_email)
        st.session_state.chat_sessions = {
            c['id']: {
                'title': c['title'],
                'created_at': c['created_at'],
                'messages': chat_db.get_chat_messages(c['id'])
            }
            for c in chats
        }
    
    if 'current_chat_id' not in st.session_state or \
       st.session_state.current_chat_id not in st.session_state.chat_sessions:
        if st.session_state.chat_sessions:
            st.session_state.current_chat_id = list(st.session_state.chat_sessions.keys())[0]
        else:
            _create_new_chat()
    
    if 'chatbot_instance' not in st.session_state:
        st.session_state.chatbot_instance = HealthChatbot()
    if 'pending_chat_query' not in st.session_state:
        st.session_state.pending_chat_query = None


def _create_new_chat():
    """Create a new chat session (saves to DB)"""
    user_email = _get_current_user_email()
    chat_id = chat_db.create_chat(user_email, "New Chat")
    
    st.session_state.chat_sessions[chat_id] = {
        'title': 'New Chat',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'messages': []
    }
    st.session_state.current_chat_id = chat_id
    return chat_id


def _delete_chat(chat_id):
    """Delete a chat session (from DB and state)"""
    chat_db.delete_chat(chat_id)
    
    if chat_id in st.session_state.chat_sessions:
        del st.session_state.chat_sessions[chat_id]
    
    if st.session_state.current_chat_id == chat_id:
        if st.session_state.chat_sessions:
            st.session_state.current_chat_id = list(st.session_state.chat_sessions.keys())[0]
        else:
            _create_new_chat()


def inject_chat_page_css():
    """Custom CSS - hide avatars, add floating back button"""
    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        section[data-testid="stSidebar"] {
            display: block !important;
            visibility: visible !important;
            background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%) !important;
            min-width: 300px !important;
        }
        
        .main .block-container {
            padding-top: 4rem;
            padding-bottom: 6rem;
            max-width: 900px;
            margin: 0 auto;
        }
        
        [data-testid="stChatMessageAvatarUser"],
        [data-testid="stChatMessageAvatarAssistant"] {
            display: none !important;
        }
        
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
        
        [data-testid="stChatInput"] {
            border-radius: 14px !important;
            border: 1px solid rgba(102, 126, 234, 0.3) !important;
        }
        
        [data-testid="stChatInput"]:focus-within {
            border-color: rgba(102, 126, 234, 0.8) !important;
        }
        
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
    
    if st.button("🏠 Back to Home", key="floating_back_btn"):
        st.session_state.show_chat_page = False
        st.rerun()
    
    with st.sidebar:
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
        st.caption(f"{chat_db.chat_count(_get_current_user_email())} chats saved")
        
        chat_items = list(st.session_state.chat_sessions.items())
        
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
            chat_db.clear_user_chats(_get_current_user_email())
            st.session_state.chat_sessions = {}
            _create_new_chat()
            st.rerun()
    
    current_chat = st.session_state.chat_sessions[st.session_state.current_chat_id]
    
    st.markdown(f"""
    <div class="chat-header">
        <div class="chat-title">🤖 MediBot</div>
        <div class="chat-subtitle">{current_chat['created_at'][:16]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.session_state.get('pending_chat_query'):
        query = st.session_state.pending_chat_query
        st.session_state.pending_chat_query = None
        _handle_message(query)
    
    if not current_chat['messages']:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h2 style="color: #ffffff;">How can I help you today?</h2>
            <p style="color: #808090;">Ask me anything about your health</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("**🌡️ Common Symptoms:**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🌡️ I have a fever", use_container_width=True):
                _handle_message("I have a fever")
        with col2:
            if st.button("🤕 I have a headache", use_container_width=True):
                _handle_message("I have a headache")
        with col3:
            if st.button("🤧 I have a cold and cough", use_container_width=True):
                _handle_message("I have a cold and cough")
        
        col4, col5, col6 = st.columns(3)
        with col4:
            if st.button("🤢 Stomach pain", use_container_width=True):
                _handle_message("I have stomach pain")
        with col5:
            if st.button("💧 I have diarrhea", use_container_width=True):
                _handle_message("I have diarrhea")
        with col6:
            if st.button("🩹 I have an allergy", use_container_width=True):
                _handle_message("I have an allergy")
        
        st.markdown("---")
        st.markdown("**🩺 Chronic Conditions:**")
        
        col7, col8, col9, col10 = st.columns(4)
        with col7:
            if st.button("🩸 Diabetes", use_container_width=True):
                _handle_message("I have diabetes, what should I do?")
        with col8:
            if st.button("💓 BP High", use_container_width=True):
                _handle_message("My blood pressure is high")
        with col9:
            if st.button("🧠 Stroke", use_container_width=True):
                _handle_message("Tell me about stroke")
        with col10:
            if st.button("🫘 Kidney", use_container_width=True):
                _handle_message("Tell me about kidney disease")
        
        st.markdown("---")
        st.markdown("**💊 Other Topics:**")
        
        col11, col12 = st.columns(2)
        with col11:
            if st.button("⚖️ Calculate my BMI", use_container_width=True):
                _handle_message("Calculate my BMI: 70 kg, 170 cm")
        with col12:
            if st.button("🚨 Emergency numbers", use_container_width=True):
                _handle_message("What are the emergency numbers in Pakistan?")
    
    for msg in current_chat['messages']:
        if msg['role'] == 'user':
            with st.chat_message("user"):
                st.markdown(msg['content'])
        else:
            with st.chat_message("assistant"):
                st.markdown(msg['content'])
    
    user_input = st.chat_input("Message MediBot...")
    
    if user_input:
        _handle_message(user_input)


def _handle_message(user_input):
    """Process user message (saves to DB)"""
    chat_id = st.session_state.current_chat_id
    current_chat = st.session_state.chat_sessions[chat_id]
    
    current_chat['messages'].append({
        'role': 'user',
        'content': user_input
    })
    chat_db.add_message(chat_id, 'user', user_input)
    
    if len(current_chat['messages']) == 1:
        title = user_input[:35]
        if len(user_input) > 35:
            title += "..."
        current_chat['title'] = title
        chat_db.update_chat_title(chat_id, title)
    
    user_email = _get_current_user_email()
    bot_response = st.session_state.chatbot_instance.get_response(user_input, user_email=user_email)
    
    current_chat['messages'].append({
        'role': 'assistant',
        'content': bot_response
    })
    chat_db.add_message(chat_id, 'assistant', bot_response)
    
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