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

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🩸 **Diabetes Prediction** | 62.38% accuracy · 100,244 patients |
| ❤️ **Heart Disease Prediction** | 88.52% accuracy ⭐ Best Model |
| 🧠 **Stroke Prediction** | 72.90% accuracy · 80% Recall |
| 🔒 **Federated Learning** | 3 hospitals train together, zero data sharing |
| 🛡️ **Differential Privacy** | Gaussian noise for (ε, δ) privacy guarantee |
| 🔍 **Explainable AI (SHAP)** | Feature importance for medical trust |
| 💬 **AI Health Chatbot** | Groq-powered bilingual (English + Roman Urdu) |
| 📄 **PDF Reports** | Downloadable medical reports |
| 📜 **Prediction History** | SQLite-based tracking for doctors |
| 🔐 **User Authentication** | bcrypt-secured doctor login + patient guest mode |
| 📞 **Contacts & Helpline** | Emergency numbers, hospitals, support |

---

## 📊 Model Performance

| Disease | Accuracy | Patients | Data Shared | Privacy |
|---------|----------|----------|-------------|---------|
| 🩸 Diabetes | 62.38% | 100,244 | 0 bytes | ✅ DP |
| ❤️ Heart Disease | **88.52%** ⭐ | 303 | 0 bytes | ✅ DP |
| 🧠 Stroke | 72.90% | 5,109 | 0 bytes | ✅ DP |

**Total:** 105,656 patients trained · **ZERO** data shared

---

## 🛠️ Tech Stack

- **AI/ML:** TensorFlow, Federated Learning (FedAvg), Differential Privacy
- **Explainability:** SHAP (SHapley Additive exPlanations)
- **Chatbot:** Groq API (Llama 3.3 70B)
- **Frontend:** Streamlit, Custom CSS
- **Database:** SQLite (history + users)
- **Auth:** bcrypt password hashing
- **PDF:** ReportLab
- **Deployment:** Streamlit Community Cloud

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/shasnainsyed183-netizen/Federated-Diabetes-Prediction.git
cd Federated-Diabetes-Prediction

python -m venv venv
venv\Scripts\activate       # Windows

pip install -r requirements.txt
echo GROQ_API_KEY=gsk_your_key_here > .env

streamlit run multi_disease_dashboard.py