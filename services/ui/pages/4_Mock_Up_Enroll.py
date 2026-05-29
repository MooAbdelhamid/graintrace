"""Mock up"""

import streamlit as st
from lib.style import (
    card,
    inject_global_css,
    page_header,
    step_header,
)

st.set_page_config(page_title="Enrol a bow — GrainTrace", page_icon="📝", layout="wide")
inject_global_css()

page_header(
    "Mockup Experiment",
    "Upload one photo of a bow get embeddings",
    section="SECTION · IDENTIFY",
)

# ===========================================================
# STEP 1 — Upload + preflight
# ===========================================================

go = False
photo_bytes: list[bytes] = []

with card():
    step_header(1, "Upload query photo(s)", "front view work best")

    uploaded = st.file_uploader(
        "Upload query images",
        type=["png"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded:
        pass
    else:
        st.info("Upload a photo of the bow head to start.")

    can_query = bool(uploaded)

    st.write("")

    go = st.button(
        "🔍  Find matches",
        type="primary",
        disabled=not can_query,
        use_container_width=False,
    )
