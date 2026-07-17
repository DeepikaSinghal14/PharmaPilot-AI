import os

import streamlit as st

from theme import inject_base_style, sidebar_brand, page_header

st.set_page_config(page_title="PharmaPilot AI | Documentation", page_icon="🧬", layout="wide")
inject_base_style()

with st.sidebar:
    sidebar_brand()

page_header("Documentation", "About This Project", "Context for reviewers, recruiters, and future contributors.")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
readme_path = os.path.join(BASE_DIR, "README.md")

st.markdown('<div class="pp-card">', unsafe_allow_html=True)
if os.path.exists(readme_path):
    with open(readme_path, "r") as f:
        st.markdown(f.read())
else:
    st.markdown("README.md not found.")
st.markdown('</div>', unsafe_allow_html=True)
