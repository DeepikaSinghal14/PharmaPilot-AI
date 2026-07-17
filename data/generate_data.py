"""
PharmaPilot AI - synthetic data generator
Generates realistic-looking (but fully fake) clinical trial data:
patients, sites, visits, protocol deviations, biomarkers.

Run: python data/generate_data.py
Writes CSVs into this same data/ folder.
"""

import os
import random
from datetime import date, timedelta

import numpy as np
import pandas as pd
from faker import Faker

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
fake = Faker()
Faker.seed(SEED)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

COUNTRIES = [
    "United States", "Germany", "France", "Spain", "Italy", "United Kingdom",
    "Poland", "Brazil", "Japan", "South Korea", "Canada", "Australia",
    "India", "Mexico", "Netherlands",
]

N_PATIENTS = 1000
N_SITES = 42
STUDY_START = date(2023, 6, 1)
TODAY = date(2025, 7, 16)

# ---------------------------------------------------------------- Sites ----
sites = []
for i in range(1, N_SITES + 1):
    country = random.choice(COUNTRIES)
    sites.append(
        {
            "Site_ID": f"S{i:03d}",
            "Country": country,
            "City": fake.city(),
            "Principal_Investigator": f"Dr. {fake.last_name()}",
            "Activation_Date": fake.date_between(start_date=STUDY_START, end_date=STUDY_START + timedelta(days=120)),
            "Target_Enrollment": random.randint(15, 45),
        }
    )
sites_df = pd.DataFrame(sites)

# ------------------------------------------------------------- Patients ----
statuses = ["Active", "Completed", "Withdrawn", "Screen Failed"]
status_weights = [0.55, 0.24, 0.13, 0.08]

patients = []
for i in range(1, N_PATIENTS + 1):
    site = sites_df.sample(1, weights=sites_df["Target_Enrollment"]).iloc[0]
    enroll_date = fake.date_between(start_date=site["Activation_Date"], end_date=TODAY)
    age = int(np.clip(np.random.normal(54, 14), 18, 89))
    sex = random.choice(["Male", "Female"])
    status = random.choices(statuses, weights=status_weights, k=1)[0]
    travel_km = round(np.random.exponential(35) + random.choice([0, 0, 0, 40, 90]), 1)
    missed_visits = np.random.poisson(0.6) if status != "Withdrawn" else np.random.poisson(2.4)

    patients.append(
        {
            "Patient_ID": f"P{i:05d}",
            "Site_ID": site["Site_ID"],
            "Country": site["Country"],
            "Age": age,
            "Sex": sex,
            "Enrollment_Date": enroll_date,
            "Status": status,
            "Travel_Distance_KM": travel_km,
            "Previous_Missed_Visits": int(missed_visits),
        }
    )
patients_df = pd.DataFrame(patients)

# --------------------------------------------------------------- Visits ----
VISIT_SCHEDULE = ["Screening", "Baseline", "Week 4", "Week 8", "Week 12", "Week 24", "Follow-up"]

visits = []
for _, p in patients_df.iterrows():
    n_visits_done = random.randint(2, len(VISIT_SCHEDULE)) if p["Status"] != "Screen Failed" else 1
    current = pd.to_datetime(p["Enrollment_Date"])
    for v_idx in range(n_visits_done):
        visit_name = VISIT_SCHEDULE[v_idx]
        completed = True
        if p["Status"] == "Withdrawn" and v_idx == n_visits_done - 1:
            completed = random.random() > 0.5
        visits.append(
            {
                "Patient_ID": p["Patient_ID"],
                "Visit": visit_name,
                "Visit_Number": v_idx + 1,
                "Scheduled_Date": current.date(),
                "Completed": completed,
            }
        )
        current += timedelta(days=random.randint(21, 40))
visits_df = pd.DataFrame(visits)

# ---------------------------------------------------------- Deviations -----
DEV_TYPES = [
    "Missed Visit Window", "Informed Consent Issue", "Dosing Error",
    "Lab Sample Handling", "Inclusion/Exclusion Violation", "Documentation Error",
]
SEVERITIES = ["Minor", "Major", "Critical"]
sev_weights = [0.65, 0.28, 0.07]

n_deviations = 260
deviations = []
for i in range(n_deviations):
    site = sites_df.sample(1).iloc[0]
    deviations.append(
        {
            "Deviation_ID": f"D{i+1:04d}",
            "Site_ID": site["Site_ID"],
            "Country": site["Country"],
            "Type": random.choice(DEV_TYPES),
            "Severity": random.choices(SEVERITIES, weights=sev_weights, k=1)[0],
            "Date_Reported": fake.date_between(start_date=site["Activation_Date"], end_date=TODAY),
        }
    )
deviations_df = pd.DataFrame(deviations)

# ---------------------------------------------------------- Biomarkers -----
BIOMARKERS = ["CRP", "HbA1c", "LDL Cholesterol", "ALT", "eGFR"]
biomarker_rows = []
for _, p in patients_df.sample(min(600, len(patients_df)), random_state=SEED).iterrows():
    for b in random.sample(BIOMARKERS, k=random.randint(1, 3)):
        baseline = {
            "CRP": np.random.normal(4, 2),
            "HbA1c": np.random.normal(6.2, 0.8),
            "LDL Cholesterol": np.random.normal(120, 25),
            "ALT": np.random.normal(28, 9),
            "eGFR": np.random.normal(85, 15),
        }[b]
        biomarker_rows.append(
            {
                "Patient_ID": p["Patient_ID"],
                "Biomarker": b,
                "Value": round(max(baseline, 0.1), 2),
                "Visit": random.choice(VISIT_SCHEDULE[:5]),
            }
        )
biomarkers_df = pd.DataFrame(biomarker_rows)

# ------------------------------------------------------------------ Save ---
patients_df.to_csv(os.path.join(OUT_DIR, "patients.csv"), index=False)
sites_df.to_csv(os.path.join(OUT_DIR, "sites.csv"), index=False)
visits_df.to_csv(os.path.join(OUT_DIR, "visits.csv"), index=False)
deviations_df.to_csv(os.path.join(OUT_DIR, "deviations.csv"), index=False)
biomarkers_df.to_csv(os.path.join(OUT_DIR, "biomarkers.csv"), index=False)

print(f"Generated: {len(patients_df)} patients, {len(sites_df)} sites, "
      f"{len(visits_df)} visits, {len(deviations_df)} deviations, "
      f"{len(biomarkers_df)} biomarker readings.")
