"""
Streamlit Chatbot UI Component for MediFederate
"""

import streamlit as st
from chatbot import HealthChatbot


def render_chatbot_tab():
    """Chatbot tab render karein"""
    st.header("💬 MediBot — AI Health Assistant")
    st.markdown("""
    **MediBot** aapki sehat ke baare mein sawalon ka jawab deta hai.
    Aap Urdu ya English mein pooch sakte hain!
    """)

    # Session state initialize karein
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {
                'role': 'assistant',
                'content': """Assalam-o-Alaikum! 🌟

Main **MediBot** hoon — aapka AI health assistant.

Aap mujhse yeh pooch sakte hain:
- 🩸 Diabetes / Sugar
- ❤️ Heart / Dil
- 🧠 Stroke / Lakwa
- ⚖️ BMI / Weight
- 💓 BP / Blood Pressure
- 🍎 Diet / Khana
- 🏃 Exercise / Walk
- 🚨 Emergency

**Kya jaanna chahte hain aap?**"""
            }
        ]

    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = HealthChatbot()

    # Quick suggestion buttons
    st.markdown("**💡 Quick Questions:**")
    col1, col2, col3, col4 = st.columns(4)
    quick_queries = [
        "Mera sugar 200 hai kya karoon?",
        "BMI calculate karein 70 kg 170 cm",
        "BP high hai kya karein?",
        "Emergency number kya hai?"
    ]
    clicked_query = None
    with col1:
        if st.button("🩸 Sugar High", key="q1"):
            clicked_query = quick_queries[0]
    with col2:
        if st.button("⚖️ Check BMI", key="q2"):
            clicked_query = quick_queries[1]
    with col3:
        if st.button("💓 BP High", key="q3"):
            clicked_query = quick_queries[2]
    with col4:
        if st.button("🚨 Emergency", key="q4"):
            clicked_query = quick_queries[3]

    st.markdown("---")

    # Chat history dikhayein
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                with st.chat_message("user"):
                    st.markdown(message['content'])
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(message['content'])

    # User input
    user_input = st.chat_input("Apna sawal likhein...")

    # Quick query handling
    if clicked_query:
        user_input = clicked_query

    if user_input:
        # User ka message add karein
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })

        # Bot ka response lein
        bot_response = st.session_state.chatbot.get_response(user_input)

        # Bot ka response add karein
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': bot_response
        })

        st.rerun()

    # Clear chat button
    if len(st.session_state.chat_history) > 1:
        if st.button("🗑️ Chat Clear Karein"):
            st.session_state.chat_history = st.session_state.chat_history[:1]
            st.rerun()