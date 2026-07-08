import streamlit as st
from lib import api_client

st.title("Identify a bow")

photo = st.file_uploader("Upload a query photo", type=["jpg", "jpeg", "png"])

if photo and st.button("Verify", type="primary"):
    try:
        result = api_client.verify(photo.getvalue(), filename=photo.name)

        st.success("Query processed")

        st.json(result)

    except Exception as e:
        st.error(f"Verification failed: {e}")
