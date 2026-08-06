"""
PharmaPilot AI - shared visual theme
Design tokens kept in one place so every page looks like the same product.
"""

import streamlit as st

# ---- Design tokens ---------------------------------------------------------
COLOR_BG = "#F4F6FA"
COLOR_PANEL = "#FFFFFF"
COLOR_BORDER = "#E4E9EF"
COLOR_NAVY = "#0B2545"
COLOR_NAVY_SOFT = "#13355C"
COLOR_TEAL = "#1E7F72"
COLOR_TEAL_SOFT = "#E7F3F1"
COLOR_AMBER = "#C97C1F"
COLOR_AMBER_SOFT = "#FBF0E1"
COLOR_RED = "#B23A48"
COLOR_RED_SOFT = "#FBEAEC"
COLOR_GREEN = "#2E8B57"
COLOR_GREEN_SOFT = "#E9F5EE"
COLOR_TEXT = "#242C35"
COLOR_MUTED = "#6B7785"

FONT_UI = "'Inter', 'Segoe UI', sans-serif"
FONT_MONO = "'IBM Plex Mono', 'Courier New', monospace"


def inject_base_style():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

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
            background-color: rgba(255,255,255,0.12) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            border-radius: 6px !important;
        }}
        section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover {{
            background-color: rgba(255,255,255,0.06) !important;
            border-radius: 6px !important;
        }}
        section[data-testid="stSidebar"] .stExpander {{
            border: 1px solid rgba(255,255,255,0.14) !important;
            border-radius: 8px !important;
            background-color: rgba(255,255,255,0.04) !important;
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
            width: 36px; height: 36px;
            border-radius: 9px;
            background: linear-gradient(135deg, {COLOR_TEAL}, {COLOR_NAVY_SOFT});
            display:flex; align-items:center; justify-content:center;
            font-family: {FONT_MONO}; font-weight:700; color:white; font-size:15px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.25);
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
            margin-bottom: 4px;
            font-weight: 600;
        }}
        .pp-title {{
            font-size: 32px;
            font-weight: 800;
            color: {COLOR_NAVY};
            margin: 0 0 6px 0;
            letter-spacing: -0.3px;
        }}
        .pp-subtitle {{
            color: {COLOR_MUTED};
            font-size: 15px;
            margin-bottom: 20px;
            max-width: 720px;
            line-height: 1.5;
        }}

        /* ---- Status banner (trial health at a glance) ---- */
        .pp-banner {{
            display: flex;
            align-items: center;
            gap: 14px;
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 22px;
            border: 1px solid var(--banner-border);
            background: var(--banner-bg);
        }}
        .pp-banner-icon {{
            font-size: 22px;
            line-height: 1;
        }}
        .pp-banner-title {{
            font-weight: 700;
            font-size: 15px;
            color: {COLOR_NAVY};
            margin-bottom: 2px;
        }}
        .pp-banner-text {{
            font-size: 13.5px;
            color: {COLOR_MUTED};
        }}

        /* KPI specimen card */
        .pp-kpi {{
            background: {COLOR_PANEL};
            border: 1px solid {COLOR_BORDER};
            border-left: 4px solid var(--accent, {COLOR_TEAL});
            border-radius: 10px;
            padding: 15px 16px 13px 16px;
            height: 100%;
            box-shadow: 0 1px 2px rgba(11,37,69,0.04);
            transition: box-shadow 0.15s ease, transform 0.15s ease;
        }}
        .pp-kpi:hover {{
            box-shadow: 0 6px 16px rgba(11,37,69,0.10);
            transform: translateY(-1px);
        }}
        .pp-kpi-top {{
            display:flex; align-items:center; justify-content:space-between;
        }}
        .pp-kpi-label {{
            font-family: {FONT_MONO};
            font-size: 10.5px;
            letter-spacing: 1.1px;
            text-transform: uppercase;
            color: {COLOR_MUTED};
            margin-bottom: 6px;
        }}
        .pp-kpi-icon {{
            font-size: 15px;
            opacity: 0.75;
        }}
        .pp-kpi-value {{
            font-family: {FONT_MONO};
            font-size: 27px;
            font-weight: 600;
            color: {COLOR_NAVY};
            line-height:1.1;
        }}
        .pp-kpi-delta {{
            font-size: 12px;
            margin-top: 5px;
            color: {COLOR_MUTED};
        }}

        /* Section card wrapper */
        .pp-card {{
            background: {COLOR_PANEL};
            border: 1px solid {COLOR_BORDER};
            border-radius: 10px;
            padding: 18px 20px;
            box-shadow: 0 1px 2px rgba(11,37,69,0.04);
            transition: box-shadow 0.15s ease;
            margin-bottom: 4px;
        }}
        .pp-card:hover {{
            box-shadow: 0 4px 14px rgba(11,37,69,0.07);
        }}
        .pp-card-note {{
            font-size: 12.5px;
            color: {COLOR_MUTED};
            margin-top: 8px;
            line-height: 1.4;
        }}
        .pp-section-label {{
            font-family: {FONT_MONO};
            font-size: 11px;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: {COLOR_MUTED};
            margin: 26px 0 10px 2px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .pp-section-label::after {{
            content: "";
            flex: 1;
            height: 1px;
            background: {COLOR_BORDER};
        }}

        /* Small pill tag, e.g. "Synthetic demo data" */
        .pp-pill {{
            display: inline-block;
            font-size: 11px;
            font-weight: 600;
            padding: 3px 10px;
            border-radius: 999px;
            background: {COLOR_TEAL_SOFT};
            color: {COLOR_TEAL};
            letter-spacing: 0.3px;
        }}

        .stDataFrame {{ border-radius: 10px; overflow:hidden; }}

        /* Nav cards at page bottom */
        .pp-nav-card {{
            background: {COLOR_PANEL};
            border: 1px solid {COLOR_BORDER};
            border-radius: 10px;
            padding: 16px 18px;
            height: 100%;
            transition: box-shadow 0.15s ease, border-color 0.15s ease;
        }}
        .pp-nav-card:hover {{
            box-shadow: 0 6px 16px rgba(11,37,69,0.09);
            border-color: {COLOR_TEAL};
        }}
        .pp-nav-card-title {{
            font-weight: 700;
            color: {COLOR_NAVY};
            font-size: 14px;
            margin-bottom: 3px;
        }}
        .pp-nav-card-desc {{
            font-size: 12.5px;
            color: {COLOR_MUTED};
            line-height: 1.4;
        }}

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
        [data-testid="stAppViewContainer"] .stExpander {{
            border: 1px solid {COLOR_BORDER} !important;
            border-radius: 10px !important;
            background: {COLOR_PANEL} !important;
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


def status_banner(level: str, title: str, text: str):
    """level: 'good' | 'watch' | 'risk' """
    styles = {
        "good": (COLOR_GREEN_SOFT, COLOR_GREEN, "✅"),
        "watch": (COLOR_AMBER_SOFT, COLOR_AMBER, "⚠️"),
        "risk": (COLOR_RED_SOFT, COLOR_RED, "🚨"),
    }
    bg, border, icon = styles.get(level, styles["watch"])
    st.markdown(
        f"""
        <div class="pp-banner" style="--banner-bg:{bg}; --banner-border:{border}44;">
            <div class="pp-banner-icon">{icon}</div>
            <div>
                <div class="pp-banner-title">{title}</div>
                <div class="pp-banner-text">{text}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, delta: str = "", accent: str = COLOR_TEAL, icon: str = ""):
    st.markdown(
        f"""
        <div class="pp-kpi" style="--accent:{accent}">
            <div class="pp-kpi-top">
                <div class="pp-kpi-label">{label}</div>
                <div class="pp-kpi-icon">{icon}</div>
            </div>
            <div class="pp-kpi-value">{value}</div>
            <div class="pp-kpi-delta">{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_label(text: str):
    st.markdown(f'<div class="pp-section-label">{text}</div>', unsafe_allow_html=True)


def pill(text: str):
    st.markdown(f'<span class="pp-pill">{text}</span>', unsafe_allow_html=True)


def nav_card(title: str, desc: str):
    st.markdown(
        f"""
        <div class="pp-nav-card">
            <div class="pp-nav-card-title">{title}</div>
            <div class="pp-nav-card-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


PLOTLY_TEMPLATE = dict(
    layout=dict(
        template="plotly_white",
        font=dict(family=FONT_UI, color=COLOR_TEXT, size=12),
        # NOTE: flattened "magic underscore" keys on purpose (title_font_color,
        # xaxis_tickfont_color, etc). app.py passes its own explicit `title=`
        # on every chart and `yaxis=dict(categoryorder=...)` on some charts —
        # nesting these under literal "title"/"xaxis"/"yaxis" keys here would
        # collide with those and raise "multiple values for keyword argument".
        title_font_color=COLOR_NAVY,
        title_font_family=FONT_UI,
        title_font_size=15,
        paper_bgcolor=COLOR_PANEL,
        plot_bgcolor=COLOR_PANEL,
        colorway=[COLOR_TEAL, COLOR_NAVY, COLOR_AMBER, "#5B8AA6", COLOR_RED, "#8FB8AE"],
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
            font=dict(color=COLOR_TEXT, size=12),
        ),
        xaxis_tickfont_color=COLOR_TEXT,
        xaxis_tickfont_size=11,
        xaxis_title_font_color=COLOR_TEXT,
        xaxis_title_font_size=12,
        xaxis_gridcolor=COLOR_BORDER,
        xaxis_linecolor=COLOR_BORDER,
        xaxis_zerolinecolor=COLOR_BORDER,
        yaxis_tickfont_color=COLOR_TEXT,
        yaxis_tickfont_size=11,
        yaxis_title_font_color=COLOR_TEXT,
        yaxis_title_font_size=12,
        yaxis_gridcolor=COLOR_BORDER,
        yaxis_linecolor=COLOR_BORDER,
        yaxis_zerolinecolor=COLOR_BORDER,
    )
)
