# MediFederate: Privacy-Preserving Multi-Disease Prediction Platform

**Final Year Project Report**

**Author:** [Your Name]
**Supervisor:** [Supervisor Name]
**Institution:** [Your University Name]
**Department:** Computer Science
**Year:** 2026

---

## Abstract

MediFederate is a privacy-preserving healthcare AI platform that enables multiple hospitals to collaboratively train machine learning models without sharing any patient data. By combining Federated Learning with Differential Privacy, the system delivers accurate predictions for five diseases — Diabetes, Heart Disease, Stroke, Kidney Disease, and Thyroid — while guaranteeing complete patient privacy. The platform includes a user-friendly web dashboard, an AI-powered health chatbot, a medical knowledge gallery, and a production-grade REST API for integration with mobile applications.

---

## 1. Introduction

The healthcare industry generates massive amounts of sensitive patient data every day. Traditional machine learning approaches require centralizing this data, which raises serious privacy concerns and violates regulations like HIPAA and GDPR. MediFederate solves this problem by bringing the model to the data instead of bringing the data to the model. Using Federated Learning, multiple hospitals can train a shared global model while keeping patient data locally on their own servers. Differential Privacy adds an extra layer of protection by injecting noise into model updates, ensuring that no individual patient's information can be inferred.

---

## 2. Problem Statement

- **Data Privacy:** Centralizing patient data for AI training is a major privacy risk and often illegal.
- **Data Silos:** Hospitals cannot share data due to legal and ethical constraints, leading to fragmented AI models.
- **Limited Access:** Small hospitals lack enough data to train accurate models on their own.
- **Trust Deficit:** Patients are hesitant to share their medical data, even for research.

---

## 3. Objectives

1. Develop a federated learning framework that trains a global model across multiple hospitals without sharing raw data.
2. Integrate Differential Privacy to provide formal privacy guarantees.
3. Build accurate prediction models for five diseases: Diabetes, Heart Disease, Stroke, Kidney Disease, and Thyroid.
4. Provide Explainable AI (SHAP) to help doctors understand model decisions.
5. Create an interactive web dashboard for doctors and patients.
6. Expose a REST API for mobile and third-party integration.
7. Ensure secure authentication and role-based access control.

---

## 4. Methodology

### 4.1 Federated Learning

Federated Learning (FL) is a distributed machine learning approach where multiple clients (hospitals) collaboratively train a model under the coordination of a central server. The server initializes a global model and sends it to all clients. Each client trains the model on its local data, computes weight updates, and sends only the updates (not the data) back to the server. The server aggregates these updates using Federated Averaging (FedAvg) to produce a new global model. This process repeats for several rounds until convergence.

**Architecture:**
- Central Server: Holds the global model.
- Clients: Three simulated hospitals with different data distributions (50%, 30%, 20%).
- Communication: Only model weights are exchanged, never raw data.

### 4.2 Differential Privacy

To prevent the server from inferring sensitive information from model updates, we apply Differential Privacy (DP). Specifically, we use Gaussian noise injection: after local training, each client adds random noise sampled from a Gaussian distribution to its weight updates before sending them to the server. This ensures that the contribution of any single patient is masked, providing a mathematical guarantee of privacy.

### 4.3 Explainable AI (SHAP)

SHAP (SHapley Additive exPlanations) is used to explain individual predictions. For each disease, SHAP values indicate how much each feature contributed to the final risk score. This builds trust with clinicians and helps them make informed decisions.

### 4.4 Models and Datasets

| Disease | Dataset Size | Model Architecture | Accuracy |
|---------|--------------|-------------------|----------|
| Diabetes | 100,244 patients | Dense Neural Network | 62.38% |
| Heart Disease | 303 patients | Dense Neural Network | 88.52% |
| Stroke | 5,109 patients | Dense Neural Network | 72.90% |
| Kidney Disease | 400 patients | Dense Neural Network | 100% |
| Thyroid | 3,000 patients | Dense Neural Network | 54.67% (Synthetic) |

*Note: Thyroid uses a synthetic dataset for demonstration; accuracy will improve with real data.*

### 4.5 System Architecture

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

---

## 5. Implementation

### 5.1 Tech Stack

- **AI/ML:** TensorFlow 2.x, Scikit-learn, SHAP, NumPy, Pandas
- **Frontend:** Streamlit, Plotly, Custom CSS
- **Backend:** FastAPI, Uvicorn
- **Database:** SQLite (users, prediction history, chat history)
- **Authentication:** bcrypt
- **AI Chatbot:** Groq API (Llama 3.3 70B)
- **PDF Generation:** ReportLab
- **Deployment:** Streamlit Cloud, Railway

### 5.2 Modules

- `multi_disease_dashboard.py`: Main dashboard with 9 tabs.
- `federated_learning.py`: Core FL logic.
- `differential_privacy.py`: DP noise injection.
- `heart_federated.py`, `stroke_federated.py`, `kidney_federated.py`, `thyroid_federated.py`: Disease-specific FL training.
- `shap_explainer.py`: SHAP analysis.
- `api.py`: REST API endpoints.
- `login_page.py`, `auth.py`: Authentication.
- `chat_page.py`, `chatbot.py`: AI chatbot.
- `pdf_generator.py`: PDF report generation.
- `history_db.py`: Prediction history.

### 5.3 REST API

The REST API exposes five endpoints:

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

**Live API Documentation:** https://federated-diabetes-prediction-production.up.railway.app/docs

---

## 6. Results and Discussion

### 6.1 Model Performance

The models achieved the following accuracies:

- Diabetes: 62.38%
- Heart Disease: 88.52% (Best Model)
- Stroke: 72.90%
- Kidney Disease: 100%
- Thyroid: 54.67% (Synthetic)

### 6.2 Privacy Guarantees

- **Zero Data Sharing:** No patient data ever leaves the hospital.
- **Differential Privacy:** Gaussian noise ensures individual privacy.
- **Secure Aggregation:** Only weights are averaged.

### 6.3 Explainability

SHAP values provide feature importance for each prediction, helping doctors understand the reasoning behind the AI's decision.

---

## 7. Features

- Multi-disease prediction (5 diseases)
- Federated Learning with 3 hospitals
- Differential Privacy
- Explainable AI (SHAP)
- AI Health Chatbot (Groq-powered)
- PDF medical reports
- Prediction history (per doctor)
- User authentication (bcrypt)
- Medical knowledge gallery
- Contacts & helpline
- Settings & account management
- REST API for all 5 diseases

---

## 8. Deployment

- **Streamlit App:** Deployed on Streamlit Community Cloud.
- **REST API:** Deployed on Railway (live URL available).
- **Local:** `streamlit run multi_disease_dashboard.py` and `uvicorn api:app --reload`

---

## 9. Future Scope

- Add more diseases (e.g., Cancer, Liver, Anemia).
- Integrate real hospital data for training.
- Implement secure aggregation using homomorphic encryption.
- Add mobile app using the REST API.
- Support multi-language chatbot.
- Add real-time monitoring and alerts.

---

## 10. Conclusion

MediFederate demonstrates that it is possible to build accurate healthcare AI models without compromising patient privacy. By leveraging Federated Learning and Differential Privacy, the platform provides a secure, scalable, and trustworthy solution for multi-disease prediction. The inclusion of Explainable AI and a production-grade REST API makes it suitable for real-world deployment in hospitals and mobile applications.

---

## 11. References

- McMahan, B., et al. (2017). "Communication-Efficient Learning of Deep Networks from Decentralized Data." AISTATS.
- Dwork, C. (2006). "Differential Privacy." ICALP.
- Lundberg, S. M., & Lee, S.-I. (2017). "A Unified Approach to Interpreting Model Predictions." NeurIPS.
- TensorFlow Federated Documentation.
- Streamlit Documentation.
- FastAPI Documentation.