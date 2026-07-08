"""GrainTrace UI — home page."""

import streamlit as st

st.set_page_config(page_title="GrainTrace", layout="wide")

st.title("GrainTrace")
st.caption("A traceable fingerprint for stringed-instrument bows.")

st.write(
    "Use the pages in the sidebar to **enrol** a new bow or **identify** an "
    "unknown one."
)
