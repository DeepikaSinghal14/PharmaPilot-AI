"""
PharmaPilot AI - Patient Dropout Risk model
Trains a small RandomForest on the synthetic patient data and saves it,
together with feature importances, for use in pages/2_AI_Insights.py.

Run: python models/train_model.py
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))

patients = pd.read_csv(os.path.join(DATA_DIR, "patients.csv"))
visits = pd.read_csv(os.path.join(DATA_DIR, "visits.csv"))

# ---- Feature engineering ---------------------------------------------------
visit_counts = visits.groupby("Patient_ID")["Visit_Number"].max().rename("Visits_Completed")
df = patients.merge(visit_counts, on="Patient_ID", how="left").fillna({"Visits_Completed": 0})

# Ground truth label: withdrawn patients are the positive ("dropout") class.
# This is synthetic data built so the label correlates with the features below
# (missed visits, travel distance, age, visit number) - enough to demonstrate
# a real, explainable model, not to make clinical claims.
df["Dropout"] = (df["Status"] == "Withdrawn").astype(int)

le_sex = LabelEncoder().fit(df["Sex"])
le_country = LabelEncoder().fit(df["Country"])

FEATURES = [
    "Age",
    "Sex_enc",
    "Country_enc",
    "Visits_Completed",
    "Previous_Missed_Visits",
    "Travel_Distance_KM",
]

df["Sex_enc"] = le_sex.transform(df["Sex"])
df["Country_enc"] = le_country.transform(df["Country"])

X = df[FEATURES]
y = df["Dropout"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

clf = RandomForestClassifier(
    n_estimators=300, max_depth=6, min_samples_leaf=5, random_state=42, class_weight="balanced"
)
clf.fit(X_train, y_train)

train_acc = clf.score(X_train, y_train)
test_acc = clf.score(X_test, y_test)
print(f"Train accuracy: {train_acc:.3f} | Test accuracy: {test_acc:.3f}")

importances = pd.Series(clf.feature_importances_, index=FEATURES).sort_values(ascending=False)
print("Feature importances:\n", importances)

joblib.dump(
    {
        "model": clf,
        "features": FEATURES,
        "le_sex": le_sex,
        "le_country": le_country,
        "importances": importances,
        "test_accuracy": test_acc,
    },
    os.path.join(MODEL_DIR, "dropout_model.pkl"),
)
print("Saved model to models/dropout_model.pkl")
