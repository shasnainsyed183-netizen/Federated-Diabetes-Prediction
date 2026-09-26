import pandas as pd

# Data load karein
df = pd.read_csv('data/diabetic_data.csv')

# 1. Faltu columns hata dein
drop_cols = ['encounter_id', 'patient_nbr', 'weight', 'payer_code', 'medical_specialty']
df = df.drop(columns=drop_cols)

# 2. Missing values (?) ko standard missing value (NaN) banayein
df = df.replace('?', pd.NA)

# 3. Race mein missing values ko 'Unknown' se fill karein
df['race'] = df['race'].fillna('Unknown')

# 4. Ab sirf un rows ko drop karein jahan Diagnosis missing hain
df = df.dropna(subset=['diag_1', 'diag_2', 'diag_3'])

# 5. Age ko number mein convert karein
age_map = {
    '[0-10)': 5, '[10-20)': 15, '[20-30)': 25, '[30-40)': 35,
    '[40-50)': 45, '[50-60)': 55, '[60-70)': 65, '[70-80)': 75,
    '[80-90)': 85, '[90-100)': 95
}
df['age'] = df['age'].map(age_map)

# 6. Gender ko 0/1 mein convert karein
df['gender'] = df['gender'].map({'Male': 1, 'Female': 0, 'Unknown/Invalid': 0})

# 7. Change aur diabetesMed ko 0/1 mein convert karein
df['change'] = df['change'].map({'Ch': 1, 'No': 0})
df['diabetesMed'] = df['diabetesMed'].map({'Yes': 1, 'No': 0})

# 8. Target variable ko convert karein (Readmitted: <30 ya >30 = 1, NO = 0)
df['readmitted'] = df['readmitted'].map({'<30': 1, '>30': 1, 'NO': 0})

# 9. Medication columns ko convert karein (No=0, Steady=1, Up=2, Down=3)
med_cols = ['metformin', 'repaglinide', 'nateglinide', 'chlorpropamide', 
            'glimepiride', 'acetohexamide', 'glipizide', 'glyburide', 
            'tolbutamide', 'pioglitazone', 'rosiglitazone', 'acarbose', 
            'miglitol', 'troglitazone', 'tolazamide', 'examide', 
            'citoglipton', 'insulin', 'glyburide-metformin', 
            'glipizide-metformin', 'glimepiride-pioglitazone', 
            'metformin-rosiglitazone', 'metformin-pioglitazone']

for col in med_cols:
    df[col] = df[col].map({'No': 0, 'Steady': 1, 'Up': 2, 'Down': 3})

# 10. Diagnosis codes ko categories mein convert karein
def map_diag(code):
    if pd.isna(code):
        return 'Other'
    code = str(code)
    if code.startswith('V') or code.startswith('E'):
        return 'Other'
    try:
        code_num = float(code)
    except:
        return 'Other'
    
    if 390 <= code_num <= 459 or code_num == 785:
        return 'Circulatory'
    elif 460 <= code_num <= 519 or code_num == 786:
        return 'Respiratory'
    elif 520 <= code_num <= 579 or code_num == 787:
        return 'Digestive'
    elif code_num == 250:
        return 'Diabetes'
    elif 800 <= code_num <= 999:
        return 'Injury'
    elif 710 <= code_num <= 739:
        return 'Musculoskeletal'
    elif 580 <= code_num <= 629 or code_num == 788:
        return 'Genitourinary'
    elif 140 <= code_num <= 239:
        return 'Neoplasms'
    else:
        return 'Other'

for col in ['diag_1', 'diag_2', 'diag_3']:
    df[col] = df[col].apply(map_diag)

# 11. Ab bache hue categorical columns ko one-hot encode karein
cat_cols = ['race', 'max_glu_serum', 'A1Cresult', 'diag_1', 'diag_2', 'diag_3']
df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

# 12. Data ka naya shape dekhein
print("--- Naya Shape (rows, columns) ---")
print(df.shape)

# 13. Data ko save karein
df.to_csv('data/cleaned_data.csv', index=False)
print("\n--- Data 'data/cleaned_data.csv' mein save ho gaya! ---")