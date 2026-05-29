"""GrainTrace — Streamlit UI entry point.

Run with:
    streamlit run streamlit_app.py
"""

import streamlit as st
from lib.mock_backend import list_bows
from lib.style import (
    DARK,
    MED,
    card,
    inject_global_css,
    page_header,
    section_badge,
)

st.set_page_config(
    page_title="GrainTrace",
    page_icon="🎻",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

# Sidebar — brand block
with st.sidebar:
    st.markdown("### 🎻 GrainTrace")
    st.markdown(
        f"<p style='color:{MED}; font-size:13px; margin-top:-8px'>"
        f"A traceable fingerprint for stringed-instrument bows</p>",
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown(
        f"<p style='color:{MED}; font-size:11px; line-height:1.6'>"
        f"Group T1<br>Distributed Systems<br>Software Project Course</p>",
        unsafe_allow_html=True,
    )

# Hero
page_header(
    "GrainTrace",
    "A traceable fingerprint for stringed-instrument bows.",
    section="GROUP T1 · DEMO",
)

# Stat strip
db = list_bows()
with card():
    section_badge("AT A GLANCE")
    st.write("")
    c1, c2, c3 = st.columns(3)
    c1.metric("Bows in database", len(db))
    c2.metric("Model version", "mock-v0.1")
    c3.metric("Embedding dimension", "256")

# Navigation cards
st.markdown("##### Choose what you'd like to do")
st.write("")

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    with card():
        st.markdown(
            f"<div style='font-size:36px; line-height:1; margin-bottom:8px'>📝</div>"
            f"<div style='font-family:Georgia,serif; font-size:20px; "
            f"font-weight:700; color:{DARK}; margin-bottom:6px'>Enrol a bow</div>"
            f"<div style='color:{MED}; font-size:14px; line-height:1.5; "
            f"margin-bottom:16px'>Register a new bow with its passport details "
            f"and head photos.</div>",
            unsafe_allow_html=True,
        )
        if st.button(
            "Open enrolment", key="enrol", use_container_width=True, type="primary"
        ):
            st.switch_page("pages/1_Enrol_Bow.py")

with col2:
    with card():
        st.markdown(
            f"<div style='font-size:36px; line-height:1; margin-bottom:8px'>🔍</div>"
            f"<div style='font-family:Georgia,serif; font-size:20px; "
            f"font-weight:700; color:{DARK}; margin-bottom:6px'>Identify a bow</div>"
            f"<div style='color:{MED}; font-size:14px; line-height:1.5; "
            f"margin-bottom:16px'>Upload a photo to find the closest match in "
            f"the database.</div>",
            unsafe_allow_html=True,
        )
        if st.button(
            "Open identification",
            key="identify",
            use_container_width=True,
            type="primary",
        ):
            st.switch_page("pages/2_Identify_Bow.py")

with col3:
    with card():
        st.markdown(
            f"<div style='font-size:36px; line-height:1; margin-bottom:8px'>📚</div>"
            f"<div style='font-family:Georgia,serif; font-size:20px; "
            f"font-weight:700; color:{DARK}; margin-bottom:6px'>Browse database</div>"
            f"<div style='color:{MED}; font-size:14px; line-height:1.5; "
            f"margin-bottom:16px'>See every registered bow, its passport, and "
            f"its photos.</div>",
            unsafe_allow_html=True,
        )
        if st.button(
            "Open database", key="browse", use_container_width=True, type="primary"
        ):
            st.switch_page("pages/3_Browse_Database.py")

st.write("")
st.markdown(
    f"<div style='color:{MED}; font-size:13px; text-align:center; "
    f"padding:12px; font-style:italic'>"
    f"This UI is wired to a mock backend — random embeddings, cosine "
    f"matching. Swap <code>lib/mock_backend.py</code> for real HTTP calls once "
    f"the model service is ready."
    f"</div>",
    unsafe_allow_html=True,
)
