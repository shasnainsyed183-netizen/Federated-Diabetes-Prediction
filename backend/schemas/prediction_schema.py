from pydantic import BaseModel, Field

class PatientData(BaseModel):
    gender: float
    age: float
    admission_type_id: float
    discharge_disposition_id: float
    admission_source_id: float
    time_in_hospital: float
    num_lab_procedures: float
    num_procedures: float
    num_medications: float
    number_outpatient: float
    number_emergency: float
    number_inpatient: float
    number_diagnoses: float
    metformin: float
    repaglinide: float
    nateglinide: float
    chlorpropamide: float
    glimepiride: float
    acetohexamide: float
    glipizide: float
    glyburide: float
    tolbutamide: float
    pioglitazone: float
    rosiglitazone: float
    acarbose: float
    miglitol: float
    troglitazone: float
    tolazamide: float
    examide: float
    citoglipton: float
    insulin: float
    glyburide_metformin: float = Field(alias="glyburide-metformin")
    glipizide_metformin: float = Field(alias="glipizide-metformin")
    glimepiride_pioglitazone: float = Field(alias="glimepiride-pioglitazone")
    metformin_rosiglitazone: float = Field(alias="metformin-rosiglitazone")
    metformin_pioglitazone: float = Field(alias="metformin-pioglitazone")
    change: float
    diabetesMed: float
    race_Asian: float
    race_Caucasian: float
    race_Hispanic: float
    race_Other: float
    race_Unknown: float
    max_glu_serum_300: float = Field(alias="max_glu_serum_>300")
    max_glu_serum_Norm: float
    A1Cresult_8: float = Field(alias="A1Cresult_>8")
    A1Cresult_Norm: float
    diag_1_Diabetes: float
    diag_1_Digestive: float
    diag_1_Genitourinary: float
    diag_1_Injury: float
    diag_1_Musculoskeletal: float
    diag_1_Neoplasms: float
    diag_1_Other: float
    diag_1_Respiratory: float
    diag_2_Diabetes: float
    diag_2_Digestive: float
    diag_2_Genitourinary: float
    diag_2_Injury: float
    diag_2_Musculoskeletal: float
    diag_2_Neoplasms: float
    diag_2_Other: float
    diag_2_Respiratory: float
    diag_3_Diabetes: float
    diag_3_Digestive: float
    diag_3_Genitourinary: float
    diag_3_Injury: float
    diag_3_Musculoskeletal: float
    diag_3_Neoplasms: float
    diag_3_Other: float
    diag_3_Respiratory: float

    class Config:
        populate_by_name = True  # Allows using either alias or field name