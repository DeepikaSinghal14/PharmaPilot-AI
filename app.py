import os

import pandas as pd
import plotly.express as px
import streamlit as st

from theme import (
    inject_base_style, sidebar_brand, page_header, kpi_card, section_label,
    PLOTLY_TEMPLATE, COLOR_TEAL, COLOR_AMBER, COLOR_RED, COLOR_NAVY,
)

st.set_page_config(
    page_title="PharmaPilot AI | Executive Summary",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_base_style()

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


@st.cache_data
def load_data():
    patients = pd.read_csv(os.path.join(DATA_DIR, "patients.csv"), parse_dates=["Enrollment_Date"])
    sites = pd.read_csv(os.path.join(DATA_DIR, "sites.csv"), parse_dates=["Activation_Date"])
    visits = pd.read_csv(os.path.join(DATA_DIR, "visits.csv"), parse_dates=["Scheduled_Date"])
    deviations = pd.read_csv(os.path.join(DATA_DIR, "deviations.csv"), parse_dates=["Date_Reported"])
    return patients, sites, visits, deviations


patients, sites, visits, deviations = load_data()

with st.sidebar:
    sidebar_brand()
    st.caption("v0.1 · Internal demo build")
    st.markdown("---")
    st.markdown("**Study**\n\nPP-2301 · Phase III · Multi-region")
    st.markdown("**Data cut**\n\n16 Jul 2026")

page_header(
    "Executive Summary",
    "PharmaPilot AI",
    "AI-powered Clinical Trial Intelligence Platform — real-time visibility across sites, patients, and risk.",
)

# --------------------------------------------------------------- KPI row ---
total_patients = len(patients)
active = (patients["Status"] == "Active").sum()
completed = (patients["Status"] == "Completed").sum()
withdrawn = (patients["Status"] == "Withdrawn").sum()
dropout_rate = withdrawn / total_patients * 100
recruitment_rate = (active + completed) / total_patients * 100
n_deviations = len(deviations)
n_countries = patients["Country"].nunique()
n_sites = sites["Site_ID"].nunique()

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    kpi_card("Total Patients", f"{total_patients:,}", "enrolled to date", COLOR_NAVY)
with c2:
    kpi_card("Recruitment Rate", f"{recruitment_rate:.0f}%", "of target reached", COLOR_TEAL)
with c3:
    kpi_card("Dropout Rate", f"{dropout_rate:.1f}%", "withdrawn patients", COLOR_AMBER if dropout_rate < 12 else COLOR_RED)
with c4:
    kpi_card("Protocol Deviations", f"{n_deviations}", "logged this study", COLOR_AMBER)
with c5:
    kpi_card("Countries", f"{n_countries}", "active regions", COLOR_TEAL)
with c6:
    kpi_card("Sites", f"{n_sites}", "activated globally", COLOR_NAVY)

st.write("")

# ----------------------------------------------------------- Charts row ---
section_label("Recruitment & Distribution")
col_a, col_b = st.columns([1.3, 1])

with col_a:
    with st.container(border=False):
        st.markdown('<div class="pp-card">', unsafe_allow_html=True)
        cum = (
            patients.sort_values("Enrollment_Date")
            .groupby("Enrollment_Date")
            .size()
            .cumsum()
            .reset_index(name="Cumulative_Patients")
        )
        fig = px.area(cum, x="Enrollment_Date", y="Cumulative_Patients")
        fig.update_traces(line_color=COLOR_TEAL, fillcolor="rgba(30,127,114,0.15)")
        fig.update_layout(**PLOTLY_TEMPLATE["layout"], height=320, title="Cumulative Enrollment Over Time")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    with st.container(border=False):
        st.markdown('<div class="pp-card">', unsafe_allow_html=True)
        status_counts = patients["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig2 = px.pie(status_counts, names="Status", values="Count", hole=0.55)
        fig2.update_layout(**PLOTLY_TEMPLATE["layout"], height=320, title="Patient Status Mix")
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

col_c, col_d = st.columns(2)
with col_c:
    st.markdown('<div class="pp-card">', unsafe_allow_html=True)
    by_country = patients["Country"].value_counts().reset_index().head(10)
    by_country.columns = ["Country", "Patients"]
    fig3 = px.bar(by_country, x="Patients", y="Country", orientation="h")
    fig3.update_traces(marker_color=COLOR_NAVY)
    fig3.update_layout(**PLOTLY_TEMPLATE["layout"], height=360, title="Top 10 Countries by Enrollment",
                        yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_d:
    st.markdown('<div class="pp-card">', unsafe_allow_html=True)
    by_site = patients["Site_ID"].value_counts().reset_index().head(10)
    by_site.columns = ["Site_ID", "Patients"]
    fig4 = px.bar(by_site, x="Patients", y="Site_ID", orientation="h")
    fig4.update_traces(marker_color=COLOR_TEAL)
    fig4.update_layout(**PLOTLY_TEMPLATE["layout"], height=360, title="Top 10 Sites by Enrollment",
                        yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")
section_label("High-Risk Signals")
risk_col1, risk_col2 = st.columns(2)
with risk_col1:
    st.markdown('<div class="pp-card">', unsafe_allow_html=True)
    st.markdown("**Sites with highest deviation counts**")
    top_dev_sites = (
        deviations.groupby("Site_ID").size().reset_index(name="Deviations")
        .sort_values("Deviations", ascending=False).head(5)
    )
    st.dataframe(top_dev_sites, hide_index=True, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with risk_col2:
    st.markdown('<div class="pp-card">', unsafe_allow_html=True)
    st.markdown("**Critical / Major deviations, last 90 days**")
    recent_cutoff = deviations["Date_Reported"].max() - pd.Timedelta(days=90)
    recent_major = deviations[
        (deviations["Date_Reported"] >= recent_cutoff) & (deviations["Severity"].isin(["Major", "Critical"]))
    ]
    st.dataframe(
        recent_major[["Deviation_ID", "Site_ID", "Type", "Severity", "Date_Reported"]]
        .sort_values("Date_Reported", ascending=False).head(8),
        hide_index=True, use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.caption("Use the sidebar to open Operational Monitoring, AI Insights, and Documentation.")
