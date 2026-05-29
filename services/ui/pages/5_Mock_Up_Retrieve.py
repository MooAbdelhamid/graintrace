"""Mockup"""

import base64

import cv2
import numpy as np
import requests
import streamlit as st
from lib.style import (
    card,
    inject_global_css,
    page_header,
    step_header,
)

VERIFY_URL = "http://127.0.0.1:8001/verify"

# ===========================================================
# PAGE CONFIG
# ===========================================================

st.set_page_config(
    page_title="Enrol a bow — GrainTrace",
    page_icon="📝",
    layout="wide",
)

inject_global_css()

page_header(
    "Mockup Experiment",
    "Upload one photo of a bow get embeddings",
    section="SECTION · IDENTIFY",
)

# ===========================================================
# STEP 1 — Upload image
# ===========================================================

with card():
    step_header(
        1,
        "Upload query photo(s)",
        "Front view works best",
    )

    uploaded_files = st.file_uploader(
        "Upload query images",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded_files:
        can_query = True
    else:
        can_query = False
        st.info("Upload a photo of the bow head to start.")

    st.write("")

    go = st.button(
        "🔍 Find matches",
        type="primary",
        disabled=not can_query,
        use_container_width=False,
    )

# ===========================================================
# STEP 2 — Send image to FastAPI
# ===========================================================

if go and can_query:
    uploaded_file = uploaded_files[0]

    # -------------------------------------------------------
    # Read uploaded image as bytes
    # -------------------------------------------------------

    file_bytes = uploaded_file.read()

    # -------------------------------------------------------
    # Preview original image
    # -------------------------------------------------------

    st.subheader("Original Image")

    st.image(
        file_bytes,
        caption=uploaded_file.name,
        use_container_width=True,
    )

    # -------------------------------------------------------
    # Build multipart/form-data request
    # -------------------------------------------------------

    files = {
        "file": (
            uploaded_file.name,
            file_bytes,
            uploaded_file.type,
        )
    }

    # -------------------------------------------------------
    # Send request
    # -------------------------------------------------------

    with st.spinner("Processing image..."):
        response = requests.post(
            VERIFY_URL,
            files=files,
        )

    if response.status_code == 200:
        st.success("Image processed successfully")

        data = response.json()

        # ---------------------------
        # Decode image
        # ---------------------------

        img_bytes = base64.b64decode(data["image"])
        img_array = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        st.subheader("Processed Image")
        st.image(img, use_container_width=True)

        # ---------------------------
        # Decode embedding
        # ---------------------------

        raw = base64.b64decode(data["embedding"])
        embedding = np.frombuffer(raw, dtype=np.float32)
        embedding = embedding.reshape(data["embedding_shape"])

        # ---------------------------
        # Show embedding stats
        # ---------------------------
        with st.expander("Embedding info"):
            st.write("Shape:", embedding.shape)
            st.write("Mean:", float(embedding.mean()))
            st.write("Norm:", float(np.linalg.norm(embedding)))

    else:
        st.error("Request failed")
        st.write(response.text)
