import os
import pandas as pd
import pickle

# Get the base directory
base_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(base_dir, '..', '..')

# Load datasets with proper paths
symptoms = pd.read_csv(os.path.join(project_root, "datasets/symtoms_df.csv"))
precaution = pd.read_csv(os.path.join(project_root, "datasets/precautions_df.csv"))
workout = pd.read_csv(os.path.join(project_root, "datasets/workout_df.csv"))
description = pd.read_csv(os.path.join(project_root, "datasets/description.csv"))
medication = pd.read_csv(os.path.join(project_root, "datasets/medications.csv"))
diet = pd.read_csv(os.path.join(project_root, "datasets/diets.csv"))
diabetes = pd.read_csv(os.path.join(project_root, "datasets/diabetes.csv"))
heart_data = pd.read_csv(os.path.join(project_root, "datasets/heart_disease_data.csv"))
kidney_data = pd.read_csv(os.path.join(project_root, "datasets/kidney Dataset.csv"))

# Load models with proper paths
svc = pickle.load(open(os.path.join(project_root, "models/svc.pkl"), 'rb'))
model = pickle.load(open(os.path.join(project_root, "models/heart.pkl"), 'rb'))
kidney_model = pickle.load(open(os.path.join(project_root, "models/kidney.pkl"), 'rb'))
classifier = pickle.load(open(os.path.join(project_root, "models/diabetes.sav"), 'rb'))

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

