import streamlit as st

st.set_page_config(
    page_title="GrainTrace",
    layout="wide",
)

# Sidebar
with st.sidebar:
    st.title("GrainTrace")
    st.caption("A traceable fingerprint for stringed-instrument bows")

    st.divider()

    st.caption(
        """
        Group T1  
        Distributed Systems  
        Software Project Course
        """
    )

# Header
st.title("GrainTrace")
st.write("A traceable fingerprint for stringed-instrument bows.")

st.divider()

# Stats
col1, col2 = st.columns(2)

col1.metric("Model version", "v1.0")
col2.metric("Embedding dimension", "256")

st.divider()

# Navigation
st.subheader("Choose an action")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("Enrol a bow")
    st.write("Register a new bow with its passport details and head photographs.")

    if st.button("Open enrolment", use_container_width=True):
        st.switch_page("pages/1_Enrol_Bow.py")

with col2:
    st.markdown("Identify a bow")
    st.write("Upload a photograph to find the closest matches in the database.")

    if st.button("Open identification", use_container_width=True):
        st.switch_page("pages/2_Identify_Bow.py")

with col3:
    st.markdown("Browse database")
    st.write("Browse all registered bows and their passport information.")

    if st.button("Open database", use_container_width=True):
        st.switch_page("pages/3_Browse_Database.py")

st.divider()

st.caption(
    "Currently connected to a mock backend. Replace the mock service "
    "with HTTP calls to connect to the real model and retrieval system."
)
