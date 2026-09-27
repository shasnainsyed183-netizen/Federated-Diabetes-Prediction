"""
MediFederate AI Health Chatbot
Rule-based medical assistant for patient queries
"""

import re


class HealthChatbot:
    def __init__(self):
        self.name = "MediBot"
        self.knowledge_base = self._load_knowledge()
        self.greetings = ['hi', 'hello', 'helo', 'salam', 'assalam', 'assalamualaikum',
                          'hey', 'aoa', 'hy', 'hai', 'welcome']

    def _load_knowledge(self):
        """Medical knowledge base"""
        return {
            'diabetes': {
                'keywords': ['diabetes', 'sugar', 'glucose', 'insulin', 'diabetic', 'sugar level'],
                'advice': [
                    "🩸 **Diabetes Management Tips:**",
                    "1. **Diet:** Meetha, chawal, aur maida kam karein",
                    "2. **Exercise:** Roz 30 minute walk karein",
                    "3. **Monitoring:** Sugar level roz check karein",
                    "4. **Medication:** Doctor ki dawai waqt par lein",
                    "5. **Water:** Din mein 8-10 glass pani piyein",
                    "",
                    "⚠️ **Emergency:** Agar sugar 300+ ho ya chakkar aayein, foran doctor se milein."
                ]
            },
            'heart': {
                'keywords': ['heart', 'dil', 'chest pain', 'cholesterol', 'cardiac', 'heart attack'],
                'advice': [
                    "❤️ **Heart Health Tips:**",
                    "1. **Diet:** Namak, tel, aur ghee kam karein",
                    "2. **Exercise:** Halki walk aur yoga karein",
                    "3. **Stress:** Meditation aur achi neend lein",
                    "4. **Checkup:** BP aur cholesterol regular check karwayein",
                    "5. **Smoking:** Foran chhor dein",
                    "",
                    "⚠️ **Emergency:** Agar seene mein dard ho ya saans phoolay, foran 1122 call karein."
                ]
            },
            'stroke': {
                'keywords': ['stroke', 'brain', 'paralysis', 'lakwa', 'brain attack', 'falij'],
                'advice': [
                    "🧠 **Stroke Prevention Tips:**",
                    "1. **BP Control:** Blood pressure normal rakhein",
                    "2. **Sugar Control:** Diabetes manage karein",
                    "3. **Exercise:** Regular physical activity",
                    "4. **Diet:** Namak aur cholesterol kam karein",
                    "5. **Checkup:** Regular health checkup karwayein",
                    "",
                    "⚠️ **Emergency (FAST Test):**",
                    "- **F**ace drooping?",
                    "- **A**rm weakness?",
                    "- **S**peech difficulty?",
                    "- **T**ime to call 1122!"
                ]
            },
            'bp': {
                'keywords': ['bp', 'blood pressure', 'hypertension', 'pressure', 'bp high', 'bp low'],
                'advice': [
                    "💓 **Blood Pressure Management:**",
                    "",
                    "**Normal BP:** 120/80 mm Hg",
                    "**High BP:** 140/90 mm Hg se zyada",
                    "",
                    "**Tips:**",
                    "1. Namak kam karein (1 chammam se kam)",
                    "2. Stress kam karein - yoga, meditation",
                    "3. Regular exercise karein",
                    "4. Smoking aur alcohol chhorein",
                    "5. BP roz check karein",
                    "6. Doctor ki dawai kabhi na chhorein"
                ]
            },
            'diet': {
                'keywords': ['diet', 'khana', 'food', 'nutrition', 'kya khana', 'khane', 'eating'],
                'advice': [
                    "🍎 **Healthy Diet Guide:**",
                    "",
                    "**Khayein (Eat):**",
                    "- Sabziyan (vegetables) - zyada",
                    "- Phal (fruits) - 2-3 roz",
                    "- Daal, chana, lobia",
                    "- Brown rice, oats, whole wheat",
                    "- Dahi, doodh (low fat)",
                    "",
                    "**Nahi Khayein (Avoid):**",
                    "- Cheeni aur meethi cheezein",
                    "- White bread, maida",
                    "- Fried food, samosa, pakora",
                    "- Cold drinks, packed juices",
                    "- Zyada namak aur tel"
                ]
            },
            'exercise': {
                'keywords': ['exercise', 'walk', 'workout', 'vyayam', 'kasrat', 'walking', 'running'],
                'advice': [
                    "🏃 **Exercise Guide:**",
                    "",
                    "**Beginner (shuru karne wale):**",
                    "- 15 minute walk, hafte mein 3 din",
                    "",
                    "**Intermediate:**",
                    "- 30 minute walk, hafte mein 5 din",
                    "",
                    "**Advanced:**",
                    "- 45 minute: walk + yoga + light weights",
                    "",
                    "**Tips:**",
                    "- Subah ya sham walk karein",
                    "- Paani saath rakhein",
                    "- Thakawat ho to rukein",
                    "- Doctor se poochein pehle"
                ]
            },
            'emergency': {
                'keywords': ['emergency', 'urgent', 'madad', 'ambulance', 'help'],
                'advice': [
                    "🚨 **EMERGENCY NUMBERS (Pakistan):**",
                    "",
                    "- **Rescue:** 1122",
                    "- **Police:** 15",
                    "- **Edhi Ambulance:** 115",
                    "- **Chhipa:** 1020",
                    "",
                    "**Kya Karein:**",
                    "1. Ghabrayen nahi",
                    "2. Patient ko aaram se litayein",
                    "3. Tight kapre dheele karein",
                    "4. Foran ambulance call karein",
                    "5. Patient ko akela na chhorein"
                ]
            },
            'bmi': {
                'keywords': ['bmi', 'weight', 'wazan', 'obesity', 'mota', 'motapa'],
                'advice': [
                    "⚖️ **Weight Management:**",
                    "",
                    "**BMI Categories:**",
                    "- Under 18.5: Underweight (kam wazan)",
                    "- 18.5 - 24.9: Normal (theek hai) ✅",
                    "- 25 - 29.9: Overweight (zyada)",
                    "- 30+: Obese (bohot zyada)",
                    "",
                    "**Tips:**",
                    "1. Meetha aur fried food kam karein",
                    "2. Roz 30 minute exercise karein",
                    "3. Zyada sabziyan aur phal khayein",
                    "4. Neend poori lein (7-8 ghante)",
                    "5. Paani zyada piyein"
                ]
            }
        }

    def _normalize(self, text):
        """Text ko lowercase aur clean karein"""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', ' ', text)
        return text

    def _is_pure_greeting(self, text):
        """Check karein ke message sirf greeting hai ya nahi (word-based)"""
        normalized = self._normalize(text)
        words = normalized.split()
        if not words:
            return False
        # Sirf greeting words ka combination ho (e.g., "assalam o alaikum")
        greeting_words = {'assalam', 'alaikum', 'o', 'u', 'alaikom',
                          'hi', 'hello', 'helo', 'salam', 'hey', 'aoa', 'hy'}
        # Kam se kam ek word greeting ka ho aur baaki bhi greeting words mein se hon
        if len(words) <= 4 and all(w in greeting_words for w in words):
            return True
        return False

    def _detect_topic(self, text):
        """User ke sawal se topic detect karein"""
        text = self._normalize(text)
        scores = {}

        for topic, data in self.knowledge_base.items():
            score = 0
            for keyword in data['keywords']:
                if keyword in text:
                    score += len(keyword)  # Lambe keyword ko zyada weight
            scores[topic] = score

        best_topic = max(scores, key=scores.get)
        if scores[best_topic] > 0:
            return best_topic
        return None

    def _check_bmi(self, weight, height):
        """BMI calculate karein"""
        height_m = height / 100
        bmi = weight / (height_m ** 2)

        if bmi < 18.5:
            category = "Underweight (kam wazan)"
            emoji = "⚠️"
        elif bmi < 25:
            category = "Normal (theek hai)"
            emoji = "✅"
        elif bmi < 30:
            category = "Overweight (zyada)"
            emoji = "⚠️"
        else:
            category = "Obese (bohot zyada)"
            emoji = "🔴"

        return bmi, category, emoji

    def get_response(self, user_message):
        """User ke message ka jawab dein"""
        if not user_message or not user_message.strip():
            return self._welcome_message()

        # 1. Greeting check (word-based)
        if self._is_pure_greeting(user_message):
            return self._welcome_message()

        # 2. BMI calculator
        normalized = self._normalize(user_message)
        bmi_match = re.search(r'(\d+)\s*kg.*?(\d+)\s*cm', normalized)
        if not bmi_match:
            bmi_match = re.search(r'(\d+)\s*(?:weight|wazan).*?(\d+)\s*(?:height|lambai|cm)', normalized)

        if bmi_match:
            weight = int(bmi_match.group(1))
            height = int(bmi_match.group(2))
            if 20 <= weight <= 300 and 100 <= height <= 250:
                bmi, category, emoji = self._check_bmi(weight, height)
                return f"""⚖️ **Aapka BMI Result:**

- **Weight:** {weight} kg
- **Height:** {height} cm
- **BMI:** {bmi:.1f}
- **Category:** {emoji} **{category}**

{'Aapka weight bilkul theek hai! Continue healthy lifestyle.' if bmi < 25 else 'Aapko weight management ki zaroorat hai. Diet aur exercise par dhyaan dein.'}

**Kya aap diet ya exercise tips chahte hain?**"""

        # 3. Topic detection
        topic = self._detect_topic(user_message)

        if topic and 'advice' in self.knowledge_base[topic]:
            advice = "\n".join(self.knowledge_base[topic]['advice'])
            return f"{advice}\n\n**Koi aur sawal hai?**"

        # 4. Default response
        return self._default_response()

    def _welcome_message(self):
        return """Assalam-o-Alaikum! 🌟

Main **MediBot** hoon — aapka AI health assistant.

Aap mujhse yeh pooch sakte hain:
- 🩸 Diabetes ke baare mein
- ❤️ Heart health ke baare mein
- 🧠 Stroke ke baare mein
- ⚖️ BMI / weight ke baare mein
- 💓 Blood pressure ke baare mein
- 🍎 Diet aur khane ke baare mein
- 🏃 Exercise ke baare mein
- 🚨 Emergency numbers

**Kya jaanna chahte hain aap?**"""

    def _default_response(self):
        return """Main aapka sawal samajh nahi paya. 🤔

**Aap in topics par pooch sakte hain:**
- 🩸 Diabetes / Sugar
- ❤️ Heart / Dil
- 🧠 Stroke / Lakwa
- ⚖️ BMI / Weight
- 💓 BP / Blood Pressure
- 🍎 Diet / Khana
- 🏃 Exercise / Walk
- 🚨 Emergency

**Misaal:** "Mera sugar 200 hai kya karoon?" ya "BMI calculate karein 70 kg 170 cm"

Aap kya poochna chahte hain?"""


# ========================================
# TESTING
# ========================================
if __name__ == "__main__":
    bot = HealthChatbot()
    print("=" * 70)
    print("MediBot - AI Health Chatbot (Testing Mode)")
    print("=" * 70)
    print()

    test_queries = [
        "Assalam o alaikum",
        "hello",
        "Mera sugar 200 hai kya karoon?",
        "BMI calculate karein 70 kg 170 cm",
        "BP high hai kya karein?",
        "Diet kya khana chahiye?",
        "Stroke ki alamat kya hai?",
        "Heart attack ke symptoms kya hain?",
        "Emergency number kya hai?",
        "Exercise kaise karein?",
        "Mota hon kaise kam karoon?",
        "Kya aapko Urdu aati hai?"
    ]

    for query in test_queries:
        response = bot.get_response(query)
        # Sirf pehli 2 lines dikhayen (test ke liye)
        first_lines = response.split("\n")[:3]
        preview = " | ".join([l for l in first_lines if l.strip()])
        print(f"👤 {query}")
        print(f"🤖 {preview}")
        print("-" * 70)