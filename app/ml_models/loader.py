import pandas as pd
import pickle

#loading datasets for Disease prediction
symptoms=pd.read_csv("datasets\symtoms_df.csv")
precaution=pd.read_csv("datasets\precautions_df.csv")
workout=pd.read_csv("datasets\workout_df.csv")
description=pd.read_csv("datasets\description.csv")
medication=pd.read_csv("datasets\medications.csv")
diet=pd.read_csv("datasets\diets.csv")
diabetes=pd.read_csv("datasets\diabetes.csv")
heart_data=pd.read_csv("datasets\heart_disease_data.csv")
kidney_data=pd.read_csv("datasets\kidney Dataset.csv")

#load model for disease prediction
svc=pickle.load(open("models\svc.pkl",'rb'))


#models for diabetes and heart defect
model=pickle.load(open("models\heart.pkl",'rb'))
kidney_model=pickle.load(open("models\kidney.pkl",'rb'))
classifier=pickle.load(open("models\diabetes.sav",'rb'))

diabetes_remedies = [
    "Diet: Balanced diet",
    "Exercise: To help improve insulin & blood pressure control",
    "Weight Management",
    "Stress Management",
    "Medication: Metformin, Sulfonylureas, Glitazones, Glinides, GLP-1, SGLT2 inhibitors, DPP-4 inhibitors",
    "Insulin Therapy: Insulin Administration",
    "Monitoring: Continuous glucose & blood glucose monitoring"
]

kidney_remedies = [
    "Diatery changes: limit sodium, phosphorus  and  potassium intake",
    "Exercise",
    "Weight Management",
    "Medications: ACE inhibitors and ARBs, SGLT2 inhibitors",
    "Dialysis",
    "Kidney Transplant",
    "Addressing underlying condition (diabetes and high bp)"
]

heart_remedies = [
    "Diet: low in saturated trans fats, sodium and choletral",
    "Exercise: Regular Physical Exercise",
    "Smoking Cessation",
    "Weight Management",
    "Medication: ACE inhibitors and ARBs, SGLT2 inhibitors, Beta blockers, Diuretics, Statins, Antiplatelets",
    "Insulin Therapy: Insulin Administration",
    "Heart Transplant"
]

