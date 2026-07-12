"""GrainTrace UI — home page."""

import streamlit as st
from datetime import datetime
from lib.api_client import get_stats, health_check

st.set_page_config(page_title="GrainTrace", layout="wide")
# st.sidebar.title("GrainTrace")


st.title("GrainTrace")
st.markdown("_A traceable fingerprint for stringed-instrument bows._")

st.divider()

st.subheader("Overview")

try:
    stats = get_stats()

    print(stats)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.metric(
            "Registered bows",
            stats["count"],
        )

    with col2:
        st.metric(
            "Last Updated",
            datetime.fromisoformat(stats["last"]).strftime("%b %d, %Y %H:%M:%S"),
        )

    with col3:
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

    # simple System Health layout
    # for col, (service, status) in zip(cols, health.items()):
    #     with col:
    #         st.metric(
    #             service.capitalize(),
    #             "Online" if status else "Offline",
    #         )

    # emoji circles (bit bulky) for Online/Offline
    # for col, (service, status) in zip(cols, health.items()):
    #     with col:
    #         circle = "🟢" if status else "🔴"
    #         st.metric(
    #             service.capitalize(),
    #             f"{circle} {'Online' if status else 'Offline'}",
    #         )

    # adjusted circles
    def colored_dot(color):
        return f'<span style="color:{color}; font-size:18px;">&#9679;</span>'

    for col, (service, status) in zip(cols, health.items()):
        with col:
            st.markdown(f"_{service.capitalize()}_")

            dot = colored_dot("green" if status else "red")
            status_text = "Online" if status else "Offline"

            st.markdown(f"{dot} {status_text}", unsafe_allow_html=True)

except Exception:
    st.warning("Health check unavailable")


st.write(
    "Use the pages in the sidebar to **enrol** a new bow or **find** yours "
    "in the **GrainTrace database**."
)
