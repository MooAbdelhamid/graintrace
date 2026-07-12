"""GrainTrace UI — home page."""

import streamlit as st
from lib.api_client import get_stats, health_check

st.set_page_config(page_title="GrainTrace", layout="wide")
# st.sidebar.title("GrainTrace")

# in case we wanna change the font
# st.markdown(
#     """
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Lora&display=swap');
#     @import url('https://fonts.googleapis.com/icon?family=Material+Icons');

#     *:not(.material-icons) {
#         font-family: 'Lora', serif !important;
#     }

#     /* Ensure material icons use the correct font */
#     .material-icons {
#         font-family: 'Material Icons' !important;
#         font-style: normal;
#         font-weight: normal;
#         font-size: 24px;
#         line-height: 1;
#         letter-spacing: normal;
#         text-transform: none;
#         display: inline-block;
#         white-space: nowrap;
#         direction: ltr;
#         -webkit-font-feature-settings: 'liga';
#         -webkit-font-smoothing: antialiased;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

st.title("GrainTrace")
st.markdown("_A traceable fingerprint for stringed-instrument bows._")


try:
    stats = get_stats()

    print(stats)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Registered bows",
            stats,
        )

    with col2:
        st.metric(
            "Embedding dimension",
            256,
        )

except Exception:
    st.warning("Unable to load statistics")


st.divider()

st.subheader("System Health")

try:
    health = health_check()

    cols = st.columns(len(health))

    for col, (service, status) in zip(cols, health.items()):
        with col:
            st.metric(
                service.capitalize(),
                "Online" if status else "Offline",
            )

except Exception:
    st.warning("Health check unavailable")


st.write(
    "Use the pages in the sidebar to **enrol** a new bow or **find** yours "
    "in the **GrainTrace database**."
)
