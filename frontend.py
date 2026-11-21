import streamlit as st
import requests
import json

# Page Configuration
st.set_page_config(page_title="MediFederate - Multi-Disease AI", page_icon="🏥", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #0056b3;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 50px;
    }
    .stButton>button:hover {
        background-color: #004494;
        color: white;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        text-align: center;
    }
    .high-risk {
        background-color: #ffcccc;
        border: 2px solid #ff0000;
        color: #990000;
    }
    .low-risk {
        background-color: #ccffcc;
        border: 2px solid #00cc00;
        color: #006600;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🏥 MediFederate")
st.sidebar.markdown("---")
st.sidebar.subheader("Select Prediction Module")
disease_module = st.sidebar.radio("", [
    "🩸 Diabetes Prediction",
    "❤️ Heart Disease (Coming Soon)",
    "🧠 Stroke (Coming Soon)",
    "🫘 Kidney Disease (Coming Soon)",
    "🦋 Thyroid (Coming Soon)"
])
st.sidebar.markdown("---")
st.sidebar.info("🔒 Powered by Privacy-Preserving Federated Learning. No patient data leaves the local hospital.")

# Main Content
if disease_module == "🩸 Diabetes Prediction":
    st.title("🩸 Federated Diabetes Readmission Prediction")
    st.markdown("""
    This module uses a **Federated Learning** model trained across multiple simulated hospitals. 
    Please enter the patient details below to predict the risk of readmission.
    """)
    st.divider()

    # Create two columns for a clean layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👤 Patient Demographics")
        age_group = st.slider("Age Group (0: 0-10 yrs, 5: 50-60 yrs, 9: 90-100 yrs)", min_value=0, max_value=9, value=5)
        
        gender = st.selectbox("Gender", ["Female (0)", "Male (1)"])
        gender_val = float(gender.split("(")[1].replace(")", ""))
        
        race = st.selectbox("Race", ["Caucasian", "Asian", "Hispanic", "Other", "Unknown"])

    with col2:
        st.subheader("🏥 Hospital Stay Details")
        time_in_hospital = st.slider("Time in Hospital (Days)", min_value=1, max_value=14, value=5)
        num_medications = st.slider("Number of Medications", min_value=1, max_value=80, value=15)
        num_lab_procedures = st.slider("Number of Lab Procedures", min_value=1, max_value=130, value=40)
        diabetes_med = st.selectbox("On Diabetes Medication?", ["Yes", "No"])
        diabetes_med_val = 1.0 if diabetes_med == "Yes" else 0.0

    st.divider()

    # Button to trigger prediction
    if st.button("🔍 Predict Readmission Risk"):
        with st.spinner("Connecting to Federated Model API..."):
            
            # Base payload: We initialize all 72 features to 0.0
            payload = {
                "gender": gender_val, "age": float(age_group), "admission_type_id": 1.0, "discharge_disposition_id": 1.0, "admission_source_id": 7.0,
                "time_in_hospital": float(time_in_hospital), "num_lab_procedures": float(num_lab_procedures), "num_procedures": 1.0, 
                "num_medications": float(num_medications), "number_outpatient": 0.0, "number_emergency": 0.0, "number_inpatient": 0.0, "number_diagnoses": 9.0,
                "metformin": 0.0, "repaglinide": 0.0, "nateglinide": 0.0, "chlorpropamide": 0.0, "glimepiride": 0.0,
                "acetohexamide": 0.0, "glipizide": 0.0, "glyburide": 0.0, "tolbutamide": 0.0, "pioglitazone": 0.0,
                "rosiglitazone": 0.0, "acarbose": 0.0, "miglitol": 0.0, "troglitazone": 0.0, "tolazamide": 0.0,
                "examide": 0.0, "citoglipton": 0.0, "insulin": 0.0, "glyburide-metformin": 0.0, "glipizide-metformin": 0.0,
                "glimepiride-pioglitazone": 0.0, "metformin-rosiglitazone": 0.0, "metformin-pioglitazone": 0.0,
                "change": 0.0, "diabetesMed": diabetes_med_val,
                "race_Asian": 1.0 if race == "Asian" else 0.0,
                "race_Caucasian": 1.0 if race == "Caucasian" else 0.0,
                "race_Hispanic": 1.0 if race == "Hispanic" else 0.0,
                "race_Other": 1.0 if race == "Other" else 0.0,
                "race_Unknown": 1.0 if race == "Unknown" else 0.0,
                "max_glu_serum_>300": 0.0, "max_glu_serum_Norm": 0.0, "A1Cresult_>8": 0.0, "A1Cresult_Norm": 0.0, 
                "diag_1_Diabetes": 1.0, "diag_1_Digestive": 0.0, "diag_1_Genitourinary": 0.0, "diag_1_Injury": 0.0, 
                "diag_1_Musculoskeletal": 0.0, "diag_1_Neoplasms": 0.0, "diag_1_Other": 0.0, "diag_1_Respiratory": 0.0, 
                "diag_2_Diabetes": 0.0, "diag_2_Digestive": 0.0, "diag_2_Genitourinary": 0.0, "diag_2_Injury": 0.0, 
                "diag_2_Musculoskeletal": 0.0, "diag_2_Neoplasms": 0.0, "diag_2_Other": 0.0, "diag_2_Respiratory": 0.0, 
                "diag_3_Diabetes": 0.0, "diag_3_Digestive": 0.0, "diag_3_Genitourinary": 0.0, "diag_3_Injury": 0.0, 
                "diag_3_Musculoskeletal": 0.0, "diag_3_Neoplasms": 0.0, "diag_3_Other": 0.0, "diag_3_Respiratory": 0.0
            }

            try:
                # Send POST request to FastAPI backend
                response = requests.post("http://127.0.0.1:8000/predict/", json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    score_percentage = result['prediction_score'] * 100
                    
                    st.markdown("### 📊 Prediction Results")
                    
                    res_col1, res_col2 = st.columns(2)
                    with res_col1:
                        st.metric(label="AI Risk Score", value=f"{score_percentage:.1f}%")
                    with res_col2:
                        status_text = "🔴 HIGH RISK" if result['prediction'] == 1 else "🟢 LOW RISK"
                        st.metric(label="Readmission Status", value=status_text)
                    
                    # Custom Result Box
                    if result['prediction'] == 1:
                        st.markdown(f"""
                        <div class="result-box high-risk">
                            <h3>⚠️ High Risk of Readmission</h3>
                            <p>{result['message']}</p>
                            <p><i>Recommendation: Schedule a follow-up appointment and review medication adherence.</i></p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="result-box low-risk">
                            <h3>✅ Low Risk of Readmission</h3>
                            <p>{result['message']}</p>
                            <p><i>Recommendation: Standard discharge procedure is sufficient.</i></p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                else:
                    st.error(f"API Error: {response.text}")
                    
            except Exception as e:
                st.error(f"Failed to connect to API. Make sure the FastAPI server is running. Error: {e}")

else:
    st.title("🚧 Module Under Construction")
    st.info("This prediction module is currently being trained using Federated Learning. It will be available soon!")
    st.image("https://cdn-icons-png.flaticon.com/512/3237/3237403.png", width=200)