"""
MediFederate AI Health Chatbot
Powered by Groq API - Real Medical AI Assistant
"""

import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)


# ========================================
# SYSTEM PROMPT (AI ko medical expert banata hai)
# ========================================
SYSTEM_PROMPT = """You are MediBot, a helpful and caring AI health assistant for a Pakistani audience.

Your job is to guide patients about their health concerns with accurate, safe, and empathetic advice.

LANGUAGE RULES (VERY IMPORTANT):
- If the user writes in English, respond in English
- If the user writes in Roman Urdu (e.g., "mujhe bukhar hai"), respond in Roman Urdu
- Match the user's language and style

RESPONSE STRUCTURE (Always follow this):
1. Brief empathetic acknowledgment
2. Possible causes (2-3 common ones)
3. Home remedies / Immediate care steps (bulleted)
4. When to see a doctor (warning signs)
5. Emergency red flags (if applicable)
6. End with: "Koi aur sawal hai? Poochein!" (if Urdu) or "Any other questions? Just ask!" (if English)

MEDICAL GUIDELINES:
- Never diagnose definitively, always say "could be" or "may indicate"
- Always recommend seeing a doctor for persistent symptoms
- For emergency symptoms (chest pain, difficulty breathing, severe bleeding, stroke signs), ALWAYS tell them to call 1122 or go to hospital IMMEDIATELY
- Include emergency numbers when relevant: Rescue 1122, Edhi 115
- Be compassionate and reassuring, but never downplay serious symptoms
- Use emojis sparingly for clarity

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
"I am a health assistant. I can only help with health-related questions. Aap kisi bimari ya sehat ke baare mein poochein."

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
            raise ValueError(
                "GROQ_API_KEY not found! Please create a .env file with:\n"
                "GROQ_API_KEY=your_key_here"
            )

        self.client = Groq(api_key=self.api_key)
        self.model = "openai/gpt-oss-120b"
        self.conversation_history = []
        self.max_history = 10

    def get_response(self, user_message):
        """Get AI response from Groq API"""
        if not user_message or not user_message.strip():
            return self._welcome_message()

        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Keep history limited
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-self.max_history * 2:]

        try:
            # Call Groq API
            messages = [{"role": "system", "content": SYSTEM_PROMPT}] + self.conversation_history

            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.5,
                max_tokens=1024,
                top_p=0.9,
            )

            bot_response = chat_completion.choices[0].message.content

            # Add bot response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": bot_response
            })

            return bot_response

        except Exception as e:
            error_msg = str(e)

            # Print full error for debugging
            print(f"\n[DEBUG] Full Error: {error_msg}\n")

            if "rate_limit" in error_msg.lower() or "429" in error_msg:
                return """Rate limit reached. Please wait 1-2 minutes and try again.

For emergencies, call 1122 immediately."""

            elif "authentication" in error_msg.lower() or "401" in error_msg or "invalid_api_key" in error_msg.lower():
                return """API key problem. Please check your Groq API key in the .env file.

Make sure the key starts with 'gsk_' and is correctly copied."""

            elif "model_not_found" in error_msg.lower() or "404" in error_msg:
                return """Model not available. Please try again later.

For emergencies, call 1122 immediately."""

            elif "connect" in error_msg.lower() or "network" in error_msg.lower() or "timeout" in error_msg.lower():
                return """Internet connection problem. Please check your internet and try again."""

            else:
                return f"""Sorry, a technical error occurred.

Error details: {error_msg[:200]}

Please try again. For emergencies, call 1122."""

    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []

    def _welcome_message(self):
        return """Hello! Welcome to MediBot

I am your AI health assistant.

You can ask me about any health concern:

- Fever, Cold, Cough
- Headache, Migraine
- Stomach Pain
- Diarrhea, Vomiting
- Allergy, Rash
- Diabetes, Sugar
- Heart Problems
- Stroke
- Blood Pressure
- Diet, Exercise
- Any other medical topic

Ask in English or Roman Urdu!

What are you experiencing?"""


# ========================================
# TESTING
# ========================================
if __name__ == "__main__":
    print("=" * 70)
    print("MediBot - Groq API Test")
    print("=" * 70)

    try:
        bot = HealthChatbot()
        print(f"Connected to Groq API")
        print(f"Model: {bot.model}")
        print(f"API Key (first 10 chars): {bot.api_key[:10]}...")
        print(f"API Key length: {len(bot.api_key)}")
        print()

        test_queries = [
            "I have fever since 2 days, what should I do?",
            "Mujhe bukhar hai kya karoon?",
            "I have severe headache and nausea",
        ]

        for query in test_queries:
            print(f"\nUser: {query}")
            response = bot.get_response(query)
            print(f"MediBot: {response[:500]}")
            print("-" * 70)

    except Exception as e:
        print(f"Fatal Error: {e}")