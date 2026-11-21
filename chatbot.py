"""
MediFederate AI Health Chatbot
Powered by Groq API (Llama 3.3 70B)
"""

import os
from groq import Groq
from dotenv import load_dotenv


# Load .env file (for local development)
load_dotenv()


def _get_api_key():
    """
    Get Groq API key from multiple sources:
    1. Streamlit Secrets (for Streamlit Cloud deployment)
    2. Environment variables / .env file (for local development)
    """
    # Try Streamlit Secrets first (Streamlit Cloud)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and 'GROQ_API_KEY' in st.secrets:
            return st.secrets['GROQ_API_KEY']
    except Exception:
        pass
    
    # Fallback to environment variable / .env file (local)
    key = os.getenv("GROQ_API_KEY")
    if key:
        return key
    
    # If nothing found, raise error
    raise ValueError(
        "GROQ_API_KEY not found. Please set it in:\n"
        "- Streamlit Secrets (for cloud deployment), OR\n"
        "- .env file (for local development)"
    )


class HealthChatbot:
    """AI Health Chatbot powered by Groq (Llama 3.3 70B)"""
    
    def __init__(self):
        api_key = _get_api_key()
        self.client = Groq(api_key=api_key)
        self.model = "openai/gpt-oss-120b"
        self.system_prompt = (
            "You are MediBot, a helpful and compassionate AI health assistant "
            "for MediFederate — a privacy-preserving multi-disease prediction platform. "
            "You provide general health information, explain medical concepts, and offer "
            "lifestyle guidance. You DO NOT diagnose diseases or prescribe medications. "
            "Always advise users to consult a qualified doctor for medical concerns. "
            "Keep your answers clear, warm, and easy to understand. "
            "If a user describes a medical emergency, immediately tell them to call 1122 (Rescue) "
            "or go to the nearest hospital."
        )
    
    def get_response(self, user_message, chat_history=None):
        """Get a response from MediBot for the given user message."""
        messages = [{"role": "system", "content": self.system_prompt}]
        
        if chat_history:
            for msg in chat_history:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
        
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"⚠️ Sorry, I couldn't process your request right now. Error: {str(e)}"
    
    def stream_response(self, user_message, chat_history=None):
        """Stream a response from MediBot token by token."""
        messages = [{"role": "system", "content": self.system_prompt}]
        
        if chat_history:
            for msg in chat_history:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
        
        messages.append({"role": "user", "content": user_message})
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
                stream=True,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"⚠️ Error: {str(e)}"