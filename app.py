import os

import pandas as pd
import plotly.express as px
import streamlit as st

from theme import (
    inject_base_style, sidebar_brand, page_header, status_banner, kpi_card,
    section_label, pill, nav_card,
    PLOTLY_TEMPLATE, COLOR_TEAL, COLOR_AMBER, COLOR_RED, COLOR_NAVY, COLOR_GREEN,
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
    st.caption("v0.2 · Internal demo build")
    st.markdown("---")
    st.markdown("**Study**\n\nPP-2301 · Phase III · Multi-region")
    st.markdown("**Data cut**\n\n16 Jul 2026")
    st.markdown("---")
    with st.expander("ℹ️ About this demo"):
        st.markdown(
            "PharmaPilot AI is a **portfolio demo**, not a production system. "
            "All patients, sites, and events below are synthetically generated — "
            "no real trial data is used anywhere in this app.\n\n"
            "It's built to show what a lightweight internal intelligence layer "
            "could look like for a clinical operations team: one place to see "
            "recruitment, operational health, and predictive dropout risk."
        )

page_header(
    "Executive Summary",
    "PharmaPilot AI",
    "AI-powered Clinical Trial Intelligence Platform — real-time visibility across sites, patients, and risk.",
)
pill("Synthetic demo data · no real patients")
st.write("")

with st.expander("🧭 New here? Start with a 30-second orientation"):
    st.markdown(
        """
        This page gives you the **executive view** of a fictional Phase III trial:

        - **Top row** — headline numbers: how recruitment is going, and whether risk is trending up or down
        - **Recruitment & Distribution** — where patients are coming from, and how enrollment is trending over time
        - **High-Risk Signals** — which sites are generating the most protocol deviations right now

        For the predictive layer — a model that flags *which individual patients*
        are likely to drop out before they do — open **AI Insights** in the sidebar.
        **Operational Monitoring** lets you drill into patient- and visit-level detail.
        """
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

recent_cutoff = deviations["Date_Reported"].max() - pd.Timedelta(days=90)
recent_major = deviations[
    (deviations["Date_Reported"] >= recent_cutoff) & (deviations["Severity"].isin(["Major", "Critical"]))
]
n_recent_major = len(recent_major)

# ---- Overall status banner: a single, plain-English read on trial health ---
if dropout_rate >= 15 or n_recent_major >= 6:
    status_banner(
        "risk",
        "Trial health: needs attention",
        f"Dropout rate is {dropout_rate:.1f}% and {n_recent_major} major/critical deviations were "
        f"logged in the last 90 days. Review High-Risk Signals below and AI Insights for at-risk patients.",
    )
elif dropout_rate >= 10 or n_recent_major >= 3:
    status_banner(
        "watch",
        "Trial health: on watch",
        f"Dropout rate ({dropout_rate:.1f}%) and recent deviations are within normal range but worth "
        f"monitoring. {n_recent_major} major/critical deviations logged in the last 90 days.",
    )
else:
    status_banner(
        "good",
        "Trial health: on track",
        f"Recruitment is progressing normally with a {dropout_rate:.1f}% dropout rate and low deviation "
        f"activity across {n_sites} active sites.",
    )

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    kpi_card("Total Patients", f"{total_patients:,}", "enrolled to date", COLOR_NAVY, "🧑‍🤝‍🧑")
with c2:
    kpi_card("Recruitment Rate", f"{recruitment_rate:.0f}%", "of target reached", COLOR_TEAL, "📈")
with c3:
    kpi_card("Dropout Rate", f"{dropout_rate:.1f}%", "withdrawn patients",
              COLOR_GREEN if dropout_rate < 8 else (COLOR_AMBER if dropout_rate < 12 else COLOR_RED), "📉")
with c4:
    kpi_card("Protocol Deviations", f"{n_deviations}", "logged this study", COLOR_AMBER, "⚠️")
with c5:
    kpi_card("Countries", f"{n_countries}", "active regions", COLOR_TEAL, "🌍")
with c6:
    kpi_card("Sites", f"{n_sites}", "activated globally", COLOR_NAVY, "🏥")

st.write("")

# ----------------------------------------------------------- Charts row ---
section_label("Recruitment & Distribution")
col_a, col_b = st.columns([1.3, 1])

with col_a:
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
    st.markdown(
        '<div class="pp-card-note">Steady upward slope = recruitment on pace. '
        'Flattening curves usually signal site or region-level enrollment issues.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="pp-card">', unsafe_allow_html=True)
    status_counts = patients["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    fig2 = px.pie(status_counts, names="Status", values="Count", hole=0.55)
    fig2.update_layout(**PLOTLY_TEMPLATE["layout"], height=320, title="Patient Status Mix")
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown(
        '<div class="pp-card-note">Share of patients currently Active, Completed, or Withdrawn.</div>',
        unsafe_allow_html=True,
    )
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
    st.markdown(
        '<div class="pp-card-note">Sites appearing here repeatedly across data cuts are '
        'candidates for a monitoring visit or retraining.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

with risk_col2:
    st.markdown('<div class="pp-card">', unsafe_allow_html=True)
    st.markdown("**Critical / Major deviations, last 90 days**")
    st.dataframe(
        recent_major[["Deviation_ID", "Site_ID", "Type", "Severity", "Date_Reported"]]
        .sort_values("Date_Reported", ascending=False).head(8),
        hide_index=True, use_container_width=True,
    )
    st.markdown(
        '<div class="pp-card-note">Filtered to Major/Critical severity only — '
        'this is the list a study director would triage first.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")
section_label("Go deeper")
n1, n2, n3 = st.columns(3)
with n1:
    st.markdown('<div class="pp-nav-card">', unsafe_allow_html=True)
    st.page_link("pages/1_Operational_Monitoring.py", label="📋 Operational Monitoring")
    st.markdown(
        '<div class="pp-nav-card-desc">Patient, visit, and deviation detail with filters.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)
with n2:
    st.markdown('<div class="pp-nav-card">', unsafe_allow_html=True)
    st.page_link("pages/2_AI_Insights.py", label="🤖 AI Insights")
    st.markdown(
        '<div class="pp-nav-card-desc">Predictive dropout risk model — which patients need attention now.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)
with n3:
    st.markdown('<div class="pp-nav-card">', unsafe_allow_html=True)
    st.page_link("pages/3_Documentation.py", label="📖 Documentation")
    st.markdown(
        '<div class="pp-nav-card-desc">How this demo works and what it would take to productionize.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)
