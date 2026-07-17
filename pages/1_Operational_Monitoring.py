import os

import pandas as pd
import plotly.express as px
import streamlit as st

from theme import (
    inject_base_style, sidebar_brand, page_header, section_label,
    PLOTLY_TEMPLATE, COLOR_TEAL, COLOR_NAVY, COLOR_AMBER,
)

st.set_page_config(page_title="PharmaPilot AI | Operational Monitoring", page_icon="🧬", layout="wide")
inject_base_style()

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


@st.cache_data
def load_data():
    patients = pd.read_csv(os.path.join(DATA_DIR, "patients.csv"), parse_dates=["Enrollment_Date"])
    visits = pd.read_csv(os.path.join(DATA_DIR, "visits.csv"), parse_dates=["Scheduled_Date"])
    deviations = pd.read_csv(os.path.join(DATA_DIR, "deviations.csv"), parse_dates=["Date_Reported"])
    sites = pd.read_csv(os.path.join(DATA_DIR, "sites.csv"), parse_dates=["Activation_Date"])
    return patients, visits, deviations, sites


patients, visits, deviations, sites = load_data()

with st.sidebar:
    sidebar_brand()

page_header(
    "Operational Monitoring",
    "Patients, Visits & Deviations",
    "Day-to-day operational view for trial management teams.",
)

tab_patients, tab_visits, tab_dev = st.tabs(["Patients", "Visits", "Deviations"])

with tab_patients:
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        country_filter = st.multiselect("Country", sorted(patients["Country"].unique()))
    with col_f2:
        status_filter = st.multiselect("Status", sorted(patients["Status"].unique()))
    with col_f3:
        site_filter = st.multiselect("Site", sorted(patients["Site_ID"].unique()))

    filtered = patients.copy()
    if country_filter:
        filtered = filtered[filtered["Country"].isin(country_filter)]
    if status_filter:
        filtered = filtered[filtered["Status"].isin(status_filter)]
    if site_filter:
        filtered = filtered[filtered["Site_ID"].isin(site_filter)]

    st.markdown('<div class="pp-card">', unsafe_allow_html=True)
    st.dataframe(filtered, hide_index=True, use_container_width=True, height=420)
    st.markdown('</div>', unsafe_allow_html=True)
    st.caption(f"Showing {len(filtered):,} of {len(patients):,} patients")

with tab_visits:
    section_label("Visit completion")
    visit_summary = visits.groupby("Visit")["Completed"].agg(["sum", "count"]).reset_index()
    visit_summary["Completion_Rate"] = (visit_summary["sum"] / visit_summary["count"] * 100).round(1)
    visit_order = ["Screening", "Baseline", "Week 4", "Week 8", "Week 12", "Week 24", "Follow-up"]
    visit_summary["Visit"] = pd.Categorical(visit_summary["Visit"], categories=visit_order, ordered=True)
    visit_summary = visit_summary.sort_values("Visit")

    col_v1, col_v2 = st.columns([1.4, 1])
    with col_v1:
        st.markdown('<div class="pp-card">', unsafe_allow_html=True)
        fig = px.bar(visit_summary, x="Visit", y="Completion_Rate")
        fig.update_traces(marker_color=COLOR_TEAL)
        fig.update_layout(**PLOTLY_TEMPLATE["layout"], height=340, title="Completion Rate by Visit (%)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_v2:
        st.markdown('<div class="pp-card">', unsafe_allow_html=True)
        st.dataframe(
            visit_summary.rename(columns={"sum": "Completed", "count": "Scheduled"}),
            hide_index=True, use_container_width=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="pp-card">', unsafe_allow_html=True)
    st.dataframe(
        visits.merge(patients[["Patient_ID", "Site_ID", "Country"]], on="Patient_ID")
        .sort_values("Scheduled_Date", ascending=False),
        hide_index=True, use_container_width=True, height=380,
    )
    st.markdown('</div>', unsafe_allow_html=True)

with tab_dev:
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown('<div class="pp-card">', unsafe_allow_html=True)
        sev_counts = deviations["Severity"].value_counts().reset_index()
        sev_counts.columns = ["Severity", "Count"]
        fig = px.bar(sev_counts, x="Severity", y="Count", category_orders={"Severity": ["Minor", "Major", "Critical"]})
        fig.update_traces(marker_color=[COLOR_TEAL, COLOR_AMBER, "#B23A48"])
        fig.update_layout(**PLOTLY_TEMPLATE["layout"], height=320, title="Deviations by Severity")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_d2:
        st.markdown('<div class="pp-card">', unsafe_allow_html=True)
        type_counts = deviations["Type"].value_counts().reset_index()
        type_counts.columns = ["Type", "Count"]
        fig2 = px.bar(type_counts, x="Count", y="Type", orientation="h")
        fig2.update_traces(marker_color=COLOR_NAVY)
        fig2.update_layout(**PLOTLY_TEMPLATE["layout"], height=320, title="Deviations by Type",
                            yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="pp-card">', unsafe_allow_html=True)
    st.dataframe(deviations.sort_values("Date_Reported", ascending=False), hide_index=True,
                 use_container_width=True, height=380)
    st.markdown('</div>', unsafe_allow_html=True)
