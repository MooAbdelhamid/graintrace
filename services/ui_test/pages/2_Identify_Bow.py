"""Identification flow — verify a bow using backend API."""

import requests
import streamlit as st

st.set_page_config(
    page_title="Identify a bow — GrainTrace",
    layout="wide",
)

st.title("Identify a bow")
st.write("Upload a bow image and find the closest matches in the database.")

st.divider()

# ===========================================================
# STEP 1 — Upload
# ===========================================================
st.subheader("1. Upload query image")

file = st.file_uploader(
    "Upload image",
    type=["jpg", "jpeg", "png"],
)

image_bytes = None

if file:
    image_bytes = file.getvalue()
    st.image(image_bytes, use_container_width=True)

st.divider()

# ===========================================================
# STEP 2 — VERIFY REQUEST
# ===========================================================
st.subheader("2. Search database")

can_run = file is not None

st.write("Send image to /verify endpoint for matching.")

result_data = None

if st.button("Find matches", type="primary", disabled=not can_run):
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}

        res = requests.post(
            "http://localhost:8001/verify/",
            files=files,
        )

        result_data = res.json()

    except Exception as e:
        st.error(f"Request failed: {e}")

st.divider()

# ===========================================================
# STEP 3 — RESULTS
# ===========================================================
if result_data:
    if result_data.get("status") != "success":
        st.error("Verification failed")

    else:
        matches = result_data.get("matches", [])

        if not matches:
            st.warning("No matches found.")

        else:
            top = matches[0]

            # ===================================================
            # TOP MATCH (SAFE STREAMLIT UI)
            # ===================================================
            st.subheader("Top match")

            col1, col2 = st.columns([1, 3])

            with col1:
                st.metric("Score", f"{top['score']:.2f}")

            with col2:
                st.markdown("Best match")
                st.write(f"**Bow ID:** {top['bow_id']}")
                st.write(f"**Maker:** {top.get('maker', 'unknown')}")
                st.write(f"**Owner:** {top.get('owner', 'unknown')}")
                st.write(f"**Type:** {top.get('bow_kind', 'unknown')}")

            st.divider()

            # ===================================================
            # FULL MATCH LIST
            # ===================================================
            st.subheader("Top matches")

            for m in matches:
                col1, col2, col3 = st.columns([1, 2, 3])

                with col1:
                    st.metric("Score", f"{m['score']:.2f}")

                with col2:
                    st.write(f"**{m['bow_id']}**")

                with col3:
                    st.write(
                        f"{m.get('maker', '')} | "
                        f"{m.get('bow_kind', '')} | "
                        f"{m.get('owner', '')}"
                    )

                st.divider()
