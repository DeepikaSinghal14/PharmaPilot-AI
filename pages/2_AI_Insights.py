import os

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from theme import (
    inject_base_style, sidebar_brand, page_header, section_label,
    PLOTLY_TEMPLATE, COLOR_TEAL, COLOR_AMBER, COLOR_RED, COLOR_NAVY,
)

st.set_page_config(page_title="PharmaPilot AI | AI Insights", page_icon="🧬", layout="wide")
inject_base_style()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_PATH = os.path.join(BASE_DIR, "models", "dropout_model.pkl")


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_patients():
    return pd.read_csv(os.path.join(DATA_DIR, "patients.csv"))


bundle = load_model()
model = bundle["model"]
features = bundle["features"]
le_sex = bundle["le_sex"]
le_country = bundle["le_country"]
importances = bundle["importances"]
test_acc = bundle["test_accuracy"]

patients = load_patients()

with st.sidebar:
    sidebar_brand()

page_header(
    "AI Insights",
    "Patient Dropout Predictor",
    "Estimates the risk that an enrolled patient discontinues before study completion, "
    "and explains which factors are driving the score.",
)

col_form, col_result = st.columns([1, 1.2])

with col_form:
    st.markdown('<div class="pp-card">', unsafe_allow_html=True)
    st.markdown("**Patient profile**")
    age = st.slider("Age", 18, 90, 58)
    sex = st.selectbox("Sex", sorted(le_sex.classes_))
    country = st.selectbox("Country", sorted(le_country.classes_))
    visit_number = st.slider("Current visit number", 1, 7, 3)
    missed_visits = st.slider("Previous missed visits", 0, 6, 1)
    travel_km = st.slider("Travel distance to site (km)", 0, 300, 35)
    predict_clicked = st.button("Predict dropout risk", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_result:
    if predict_clicked:
        row = pd.DataFrame(
            [{
                "Age": age,
                "Sex_enc": le_sex.transform([sex])[0],
                "Country_enc": le_country.transform([country])[0],
                "Visits_Completed": visit_number,
                "Previous_Missed_Visits": missed_visits,
                "Travel_Distance_KM": travel_km,
            }]
        )[features]

        proba = model.predict_proba(row)[0][1]
        risk_pct = proba * 100

        if risk_pct >= 60:
            accent, label = COLOR_RED, "High risk"
        elif risk_pct >= 30:
            accent, label = COLOR_AMBER, "Watch"
        else:
            accent, label = COLOR_TEAL, "Low risk"

        st.markdown(
            f"""
            <div class="pp-kpi" style="--accent:{accent}; padding:22px 22px 18px 22px;">
                <div class="pp-kpi-label">Dropout Risk &nbsp;·&nbsp; {label}</div>
                <div class="pp-kpi-value" style="font-size:44px;">{risk_pct:.0f}%</div>
                <div class="pp-kpi-delta">Model test accuracy: {test_acc*100:.0f}% on held-out patients</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        st.markdown('<div class="pp-card">', unsafe_allow_html=True)
        st.markdown("**Most important reasons (model-wide feature importance)**")
        imp_df = importances.rename_axis("Feature").reset_index(name="Importance")
        imp_df["Feature"] = imp_df["Feature"].replace({
            "Previous_Missed_Visits": "Previous missed visits",
            "Travel_Distance_KM": "Travel distance",
            "Age": "Age",
            "Visits_Completed": "Visit number",
            "Country_enc": "Country / site history",
            "Sex_enc": "Sex",
        })
        fig = px.bar(imp_df.sort_values("Importance"), x="Importance", y="Feature", orientation="h")
        fig.update_traces(marker_color=COLOR_NAVY)
        fig.update_layout(**PLOTLY_TEMPLATE["layout"], height=280, title=None)
        st.plotly_chart(fig, use_container_width=True)
        top3 = imp_df.sort_values("Importance", ascending=False).head(3)["Feature"].tolist()
        st.markdown("Top drivers for this prediction, in order:")
        for t in top3:
            st.markdown(f"- {t}")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="pp-card">', unsafe_allow_html=True)
        st.markdown("Fill in the patient profile and click **Predict dropout risk** to see a score.")
        st.markdown('</div>', unsafe_allow_html=True)

st.write("")
section_label("Model overview")
st.markdown('<div class="pp-card">', unsafe_allow_html=True)
st.markdown(
    f"""
A Random Forest classifier trained on {len(patients):,} synthetic patient records, using enrollment,
travel, and visit-history features to estimate discontinuation risk. Held-out test accuracy: **{test_acc*100:.0f}%**.
This is a demonstration model on synthetic data — not a validated clinical prediction tool.
    """
)
st.markdown('</div>', unsafe_allow_html=True)
