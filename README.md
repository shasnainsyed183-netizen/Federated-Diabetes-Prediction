# 🏥 MediFederate

### Privacy-Preserving Multi-Disease AI Platform

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Streamlit_Cloud-FF4B4B?style=for-the-badge)](https://federated-diabetes-prediction-a2xkixwcd2dm56fjfwp5gw.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)

---

## 🎯 What is MediFederate?

MediFederate is a **privacy-preserving healthcare AI platform** that enables multiple hospitals to collaboratively train AI models **without sharing any patient data**.

Built with **Federated Learning** + **Differential Privacy** to deliver accurate medical predictions while preserving complete patient privacy.

### 🚀 **[Try the Live Demo →](https://federated-diabetes-prediction-a2xkixwcd2dm56fjfwp5gw.streamlit.app)**

### 🌐 **[Live REST API (Swagger UI) →](https://federated-diabetes-prediction-production.up.railway.app/docs)**

---

## 📸 Screenshots

### 📊 Dashboard Overview
![Dashboard Overview](screenshots/dashboard_overview.png)
*Real-time performance metrics for 5 disease prediction models — all achieving high accuracy without sharing any patient data.*

### 🩸 Diabetes Prediction
![Diabetes Prediction](screenshots/diabetes_prediction.png)
*Interactive patient input form with instant AI prediction and downloadable PDF medical report.*

### 💬 AI Health Chatbot
![AI Chatbot](screenshots/chatbot.png)
*MediBot — an intelligent health assistant powered by Groq AI, available 24/7 with full conversation history.*

### ⚙️ Settings & Account
![Settings Popup](screenshots/settings_popup.png)
*Complete account management with Profile, Security, Preferences, and Activity tabs.*

### 🏥 Medical Knowledge Gallery
![Medical Gallery](screenshots/gallery.png)
*Curated medical knowledge cards with AI chatbot integration for instant topic-based answers.*

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🩸 **Diabetes Prediction** | 62.38% accuracy · 100,244 patients |
| ❤️ **Heart Disease Prediction** | 88.52% accuracy ⭐ Best Model |
| 🧠 **Stroke Prediction** | 72.90% accuracy · 80% Recall |
| 🫘 **Kidney Disease Prediction** | 100% accuracy · 400 patients |
| 🧬 **Thyroid Prediction** | 54.67% accuracy · 3,000 patients |
| 🔒 **Federated Learning** | 3 hospitals train together, zero data sharing |
| 🛡️ **Differential Privacy** | Gaussian noise for privacy guarantee |
| 🔍 **Explainable AI (SHAP)** | Feature importance for medical trust |
| 💬 **AI Health Chatbot** | Groq-powered English chatbot with persistent history |
| 📄 **PDF Reports** | Downloadable medical reports with doctor notes |
| 📜 **Prediction History** | Per-doctor SQLite-based tracking |
| 🔐 **User Authentication** | bcrypt-secured login + patient guest mode |
| 📞 **Contacts & Helpline** | Emergency numbers and hospital directory |
| 🎨 **Settings & Account** | Profile, password change, and preferences |
| 🌐 **REST API** | Production-grade API for all 5 disease predictions |

---

## 📊 Model Performance

| Disease | Accuracy | Patients | Data Shared | Privacy |
|---------|----------|----------|-------------|---------|
| 🩸 Diabetes | 62.38% | 100,244 | 0 bytes | ✅ DP |
| ❤️ Heart Disease | **88.52%** ⭐ | 303 | 0 bytes | ✅ DP |
| 🧠 Stroke | 72.90% | 5,109 | 0 bytes | ✅ DP |
| 🫘 Kidney Disease | **100%** | 400 | 0 bytes | ✅ DP |
| 🧬 Thyroid | 54.67% | 3,000 | 0 bytes | ✅ DP |

**Total:** 108,656 patients trained · **ZERO** data shared

---

## 🛠️ Tech Stack

**AI & Machine Learning:**
- TensorFlow 2.x — Neural Networks
- Federated Averaging (FedAvg)
- Differential Privacy (Gaussian Noise)
- SHAP — Explainability
- Scikit-learn — Preprocessing

**Frontend & UI:**
- Streamlit 1.x
- Custom CSS + Animations
- Plotly Interactive Charts

**Backend & API:**
- FastAPI
- Uvicorn

**Data & Storage:**
- SQLite — History + Users + Chats
- Pandas + NumPy
- ReportLab — PDF Generation

**Security & AI Chat:**
- bcrypt — Password Hashing
- Groq API (Llama 3.3 70B)
- Python-dotenv — Secrets Management

**Deployment:**
- Streamlit Community Cloud
- Railway
- Git + GitHub

---

## 📁 Project Structure

```text
Federated_Diabetes_Project/
│
├── screenshots/                 # Project screenshots
│   ├── dashboard_overview.png
│   ├── diabetes_prediction.png
│   ├── chatbot.png
│   ├── settings_popup.png
│   └── gallery.png
│
├── data/                        # Datasets
│   ├── diabetic_data.csv
│   ├── cleaned_data.csv
│   ├── heart_disease.csv
│   ├── stroke_data.csv
│   ├── kidney_data.csv
│   └── thyroid_data.csv
│
├── multi_disease_dashboard.py   # Main dashboard (9 tabs)
├── login_page.py                # Authentication UI
├── chat_page.py                 # Full-page AI chatbot
├── chatbot.py                   # Groq AI backend
├── chat_history_db.py           # Chat persistence
├── settings_page.py             # Settings popup
├── info_pages.py                # Email & Website pages
├── legal_pages.py               # Privacy & Terms pages
├── pdf_generator.py             # PDF report generator
├── history_db.py                # Prediction history
├── auth.py                      # User authentication
├── ui_helpers.py                # UI components & charts
│
├── federated_learning.py        # Federated Learning
├── differential_privacy.py      # DP implementation
├── heart_federated.py           # Heart model training
├── stroke_federated.py          # Stroke model training
├── kidney_federated.py          # Kidney model training
├── download_thyroid_data.py     # Thyroid data preprocessing
├── thyroid_federated.py         # Thyroid model training
├── shap_explainer.py            # SHAP analysis
│
├── api.py                       # REST API (FastAPI)
├── railway.json                 # Railway deployment config
├── Procfile                     # Process file for deployment
├── requirements.txt
├── README.md
└── PROJECT_REPORT.md
```

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/shasnainsyed183-netizen/Federated-Diabetes-Prediction.git
cd Federated-Diabetes-Prediction

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add Groq API key
echo GROQ_API_KEY=gsk_your_key_here > .env

# 5. Run the Streamlit app
streamlit run multi_disease_dashboard.py

# 6. Run the REST API (Optional, in a new terminal)
uvicorn api:app --reload
```

---

## 🌐 REST API

MediFederate also provides a production-grade REST API for all 5 disease predictions.

**🌍 Live API URL:** 
https://federated-diabetes-prediction-production.up.railway.app

**📖 Live Interactive Documentation (Swagger UI):** 
https://federated-diabetes-prediction-production.up.railway.app/docs

**🖥️ Local API Documentation:**
Once the server is running locally, open your browser and go to:
```text
http://127.0.0.1:8000/docs
```

**Available Endpoints:**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/predict/diabetes` | Predict Diabetes Readmission Risk |
| POST | `/predict/heart` | Predict Heart Disease Risk |
| POST | `/predict/stroke` | Predict Stroke Risk |
| POST | `/predict/kidney` | Predict Kidney Disease Risk |
| POST | `/predict/thyroid` | Predict Thyroid Disease Risk |

**Sample Response:**
```json
{
  "disease": "Heart Disease",
  "probability": 55.4,
  "risk_level": "High Risk",
  "data_shared": "0 bytes",
  "privacy": "Differential Privacy Enabled"
}
```

---

## 🏗️ Federated Learning Architecture

```text
┌───────────────────────────────────────────────────────────┐
│            GLOBAL MODEL (Central Server)                  │
└───────────────────────────────────────────────────────────┘
         ↓              ↓              ↓
   ┌───────────┐   ┌───────────┐   ┌───────────┐
   │ Hosp. A   │   │ Hosp. B   │   │ Hosp. C   │
   │ 40K pts   │   │ 24K pts   │   │ 16K pts   │
   └───────────┘   └───────────┘   └───────────┘
         ↓              ↓              ↓
   [Local Train + Weight Clipping + DP Noise]
         ↓              ↓              ↓
   ┌───────────────────────────────────────────┐
   │   FedAvg: Average of Weights              │
   │   (No patient data transferred)           │
   └───────────────────────────────────────────┘
```