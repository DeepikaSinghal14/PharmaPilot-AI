"""
PharmaPilot AI - shared visual theme
Design tokens kept in one place so every page looks like the same product.
"""

import streamlit as st

# ---- Design tokens ---------------------------------------------------------
COLOR_BG = "#F5F7FA"
COLOR_PANEL = "#FFFFFF"
COLOR_BORDER = "#E1E7ED"
COLOR_NAVY = "#0B2545"
COLOR_NAVY_SOFT = "#13355C"
COLOR_TEAL = "#1E7F72"
COLOR_AMBER = "#C97C1F"
COLOR_RED = "#B23A48"
COLOR_TEXT = "#2B333B"
COLOR_MUTED = "#6B7785"

FONT_UI = "'Inter', 'Segoe UI', sans-serif"
FONT_MONO = "'IBM Plex Mono', 'Courier New', monospace"


def inject_base_style():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

        html, body, [class*="css"] {{
            font-family: {FONT_UI};
            color: {COLOR_TEXT};
        }}

        .stApp {{
            background-color: {COLOR_BG};
        }}

        /* ---- Sidebar ---- */
        section[data-testid="stSidebar"] {{
            background-color: {COLOR_NAVY};
        }}
        section[data-testid="stSidebar"] * {{
            color: #E7EDF3 !important;
        }}
        section[data-testid="stSidebar"] .stMarkdown small {{
            color: #9FB2C6 !important;
        }}

        /* Streamlit's auto-generated page nav links need extra-specific
           targeting - they don't always inherit from the wildcard above. */
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a,
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a span,
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a p,
        section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"],
        section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] span,
        section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] p,
        section[data-testid="stSidebar"] li a,
        section[data-testid="stSidebar"] li span {{
            color: #E7EDF3 !important;
        }}
        section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"],
        section[data-testid="stSidebar"] li a[aria-current="page"] {{
            background-color: rgba(255,255,255,0.10) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }}

        /* Header eyebrow / brand block */
        .pp-brand {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 4px 0 18px 0;
            border-bottom: 1px solid rgba(255,255,255,0.12);
            margin-bottom: 14px;
        }}
        .pp-brand-mark {{
            width: 34px; height: 34px;
            border-radius: 7px;
            background: linear-gradient(135deg, {COLOR_TEAL}, {COLOR_NAVY_SOFT});
            display:flex; align-items:center; justify-content:center;
            font-family: {FONT_MONO}; font-weight:600; color:white; font-size:15px;
        }}
        .pp-brand-name {{ font-weight:700; font-size:16px; letter-spacing:0.2px; }}
        .pp-brand-sub {{ font-size:11px; color:#9FB2C6; letter-spacing:0.4px; text-transform:uppercase; }}

        /* Page title block */
        .pp-eyebrow {{
            font-family: {FONT_MONO};
            font-size: 12px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            color: {COLOR_TEAL};
            margin-bottom: 2px;
        }}
        .pp-title {{
            font-size: 30px;
            font-weight: 700;
            color: {COLOR_NAVY};
            margin: 0 0 4px 0;
        }}
        .pp-subtitle {{
            color: {COLOR_MUTED};
            font-size: 14.5px;
            margin-bottom: 18px;
        }}

        /* KPI specimen card */
        .pp-kpi {{
            background: {COLOR_PANEL};
            border: 1px solid {COLOR_BORDER};
            border-left: 4px solid var(--accent, {COLOR_TEAL});
            border-radius: 8px;
            padding: 14px 16px 12px 16px;
            height: 100%;
        }}
        .pp-kpi-label {{
            font-family: {FONT_MONO};
            font-size: 10.5px;
            letter-spacing: 1.1px;
            text-transform: uppercase;
            color: {COLOR_MUTED};
            margin-bottom: 6px;
        }}
        .pp-kpi-value {{
            font-family: {FONT_MONO};
            font-size: 26px;
            font-weight: 600;
            color: {COLOR_NAVY};
            line-height:1.1;
        }}
        .pp-kpi-delta {{
            font-size: 12px;
            margin-top: 4px;
            color: {COLOR_MUTED};
        }}

        /* Section card wrapper */
        .pp-card {{
            background: {COLOR_PANEL};
            border: 1px solid {COLOR_BORDER};
            border-radius: 8px;
            padding: 18px 20px;
        }}
        .pp-section-label {{
            font-family: {FONT_MONO};
            font-size: 11px;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: {COLOR_MUTED};
            margin: 22px 0 8px 2px;
        }}

        .stDataFrame {{ border-radius: 8px; overflow:hidden; }}

        /* ---- Main content area: force readable text regardless of the
           viewer's OS/browser dark-mode setting. ---- */
        [data-testid="stAppViewContainer"] h1,
        [data-testid="stAppViewContainer"] h2,
        [data-testid="stAppViewContainer"] h3,
        [data-testid="stAppViewContainer"] h4,
        [data-testid="stAppViewContainer"] h5,
        [data-testid="stAppViewContainer"] h6 {{
            color: {COLOR_NAVY} !important;
        }}
        [data-testid="stAppViewContainer"] p,
        [data-testid="stAppViewContainer"] li,
        [data-testid="stAppViewContainer"] span,
        [data-testid="stAppViewContainer"] label,
        [data-testid="stAppViewContainer"] .stMarkdown {{
            color: {COLOR_TEXT} !important;
        }}
        [data-testid="stAppViewContainer"] code {{
            color: {COLOR_NAVY} !important;
            background: #EEF2F6 !important;
        }}
        [data-testid="stAppViewContainer"] a {{
            color: {COLOR_TEAL} !important;
        }}

        footer {{visibility: hidden;}}
        #MainMenu {{visibility: hidden;}}
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_brand():
    st.markdown(
        f"""
        <div class="pp-brand">
            <div class="pp-brand-mark">PP</div>
            <div>
                <div class="pp-brand-name">PharmaPilot AI</div>
                <div class="pp-brand-sub">Clinical Trial Intelligence</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(eyebrow: str, title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="pp-eyebrow">{eyebrow}</div>
        <div class="pp-title">{title}</div>
        <div class="pp-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, delta: str = "", accent: str = COLOR_TEAL):
    st.markdown(
        f"""
        <div class="pp-kpi" style="--accent:{accent}">
            <div class="pp-kpi-label">{label}</div>
            <div class="pp-kpi-value">{value}</div>
            <div class="pp-kpi-delta">{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_label(text: str):
    st.markdown(f'<div class="pp-section-label">{text}</div>', unsafe_allow_html=True)


PLOTLY_TEMPLATE = dict(
    layout=dict(
        font=dict(family=FONT_UI, color=COLOR_TEXT, size=12),
        paper_bgcolor=COLOR_PANEL,
        plot_bgcolor=COLOR_PANEL,
        colorway=[COLOR_TEAL, COLOR_NAVY, COLOR_AMBER, "#5B8AA6", COLOR_RED, "#8FB8AE"],
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
)
