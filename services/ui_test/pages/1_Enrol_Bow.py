"""Enrolment flow — register a new bow (API version)."""

import requests
import streamlit as st

st.set_page_config(
    page_title="Enrol a bow — GrainTrace",
    layout="wide",
)

st.title("Enrol a new bow")
st.write("Upload one image and enter bow metadata.")

st.divider()

# ===========================================================
# BASIC INFO
# ===========================================================
st.subheader("Bow details")

col1, col2 = st.columns(2)

with col1:
    maker = st.text_input("Maker", placeholder="e.g. Sartory")
    bow_kind = st.text_input("Bow type", placeholder="e.g. Violin bow")

with col2:
    owner = st.text_input("Owner")

st.divider()

# ===========================================================
# IMAGE INPUT (SINGLE IMAGE ONLY)
# ===========================================================
st.subheader("Bow image")

file = st.file_uploader(
    "Upload one image",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=False,
)

if file:
    st.image(file.getvalue(), use_container_width=True)

st.divider()

# ===========================================================
# SUBMIT
# ===========================================================
st.subheader("Register")

can_submit = bool(file and maker)

st.write("Send request to /register API")

response_data = None

if st.button("Register bow", type="primary", disabled=not can_submit):
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}

        data = {
            "maker": maker,
            "bow_kind": bow_kind,
            "owner": owner,
        }

        res = requests.post(
            "http://localhost:8001/register/",
            files=files,
            data=data,
        )

        response_data = res.json()

    except Exception as e:
        st.error(f"Request failed: {e}")

st.divider()

# ===========================================================
# RESPONSE
# ===========================================================
if response_data:
    st.subheader("Result")

    if response_data.get("status") == "success":
        st.success(response_data.get("message", "Registered successfully"))

    st.json(response_data)

    st.write("### Summary")
    st.write("Bow ID:", response_data.get("bow_id"))
    st.write("Maker:", response_data.get("maker"))
    st.write("Embedding size:", response_data.get("embedding_dimension"))
