"""
MediFederate AI Health Chatbot
Powered by Groq API - Real Medical AI Assistant (English only)
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv(override=True)


SYSTEM_PROMPT = """You are MediBot, a helpful and caring AI health assistant.

Your job is to guide patients about their health concerns with accurate, safe, and empathetic advice.

LANGUAGE RULES (VERY IMPORTANT):
- You MUST respond ONLY in English
- Even if the user writes in another language, respond in English
- Keep the language simple and clear

RESPONSE STRUCTURE (Always follow this):
1. Brief empathetic acknowledgment
2. Possible causes (2-3 common ones)
3. Home remedies / Immediate care steps (bulleted)
4. When to see a doctor (warning signs)
5. Emergency red flags (if applicable)
6. End with: "Do you have any other questions?"

MEDICAL GUIDELINES:
- Never diagnose definitively, always say "could be" or "may indicate"
- Always recommend seeing a doctor for persistent symptoms
- For emergency symptoms (chest pain, difficulty breathing, severe bleeding, stroke signs), ALWAYS tell them to call 1122 or go to hospital IMMEDIATELY
- Include emergency numbers when relevant: Rescue 1122, Edhi 115
- Be compassionate and reassuring, but never downplay serious symptoms

COVERAGE:
You can help with ANY health concern including but not limited to:
- Fever, cold, cough, flu
- Headache, migraine
- Stomach pain, acidity, gas
- Diarrhea, vomiting, food poisoning
- Allergy, skin rash, itching
- Diabetes, blood sugar
- Heart problems, chest pain
- Stroke
- Blood pressure
- Asthma, breathing issues
- Joint pain, back pain
- Mental health (anxiety, stress, depression)
- Women's health
- Children's health
- Diet and nutrition
- Exercise and weight management
- First aid
- And any other medical topic

If the user asks something non-medical, politely say:
"I am a health assistant. I can only help with health-related questions."

FORMAT:
- Use **bold** for important terms
- Use bullet points for lists
- Keep responses focused and clear
- For BMI: BMI = weight(kg) / (height(m))^2
  - < 18.5: Underweight
  - 18.5-24.9: Normal
  - 25-29.9: Overweight
  - 30+: Obese

Remember: You are talking to real people with real health concerns. Be kind, be accurate, be helpful."""


class HealthChatbot:
    def __init__(self):
        self.name = "MediBot"
        self.api_key = os.getenv("GROQ_API_KEY")

        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")

        self.client = Groq(api_key=self.api_key)
        self.model = "openai/gpt-oss-120b"
        self.conversation_history = []
        self.max_history = 10

    def _get_user_context(self, user_email):
        """Fetch user's recent predictions to give context to AI"""
        if not user_email:
            return ""
        
        try:
            import history_db as hist
            df = hist.get_user_predictions(user_email, limit=5)
            
            if df.empty:
                return "\n\nUSER CONTEXT: This user has no previous predictions in the system yet."
            
            context = "\n\nUSER'S RECENT PREDICTIONS:\n"
            for _, row in df.iterrows():
                prob = row['probability'] * 100 if row['probability'] <= 1 else row['probability']
                context += f"- {row['disease']}: {row['risk_level']} ({prob:.1f}%) on {row['timestamp']}\n"
            
            context += (
                "\nIf the user asks about their previous predictions, health history, or "
                "trends, use this information to answer accurately. "
                "Do NOT invent predictions that are not in this list."
            )
            return context
        
        except Exception as e:
            print(f"[History context error]: {e}")
            return ""

    def get_response(self, user_message, user_email=None):
        """Get AI response from Groq API (with user context if email provided)"""
        if not user_message or not user_message.strip():
            return self._welcome_message()

        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-self.max_history * 2:]

        try:
            user_context = self._get_user_context(user_email)
            full_system = SYSTEM_PROMPT + user_context
            
            messages = [{"role": "system", "content": full_system}] + self.conversation_history

            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.5,
                max_tokens=1024,
                top_p=0.9,
            )

            bot_response = chat_completion.choices[0].message.content

            self.conversation_history.append({
                "role": "assistant",
                "content": bot_response
            })

            return bot_response

        except Exception as e:
            error_msg = str(e)
            print(f"\n[DEBUG] Full Error: {error_msg}\n")

            if "rate_limit" in error_msg.lower() or "429" in error_msg:
                return "Rate limit reached. Please wait 1-2 minutes and try again."
            elif "authentication" in error_msg.lower() or "401" in error_msg:
                return "API key problem. Please check your Groq API key."
            elif "model_not_found" in error_msg.lower() or "404" in error_msg:
                return "Model not available. Please try again later."
            elif "connect" in error_msg.lower() or "timeout" in error_msg.lower():
                return "Internet connection problem. Please try again."
            else:
                return f"Sorry, a technical error occurred.\n\nError: {error_msg[:200]}"

    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []

    def _welcome_message(self):
        return """Hello! Welcome to MediBot

I am your AI health assistant.

You can ask me about any health concern or about your previous predictions.

What are you experiencing?"""


if __name__ == "__main__":
    print("Testing MediBot (English only)...")
    bot = HealthChatbot()
    
    print("\nTest 1: New user")
    print(bot.get_response("I have a fever, what should I do?", user_email="newuser@test.com")[:200])
    
    print("\nTest 2: User with history")
    print(bot.get_response("What was my last prediction?", user_email="test@medifederate.com")[:300])