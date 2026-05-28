"""Browse the registered bow database."""
import pandas as pd
import streamlit as st

from lib.style import (
    inject_global_css, page_header, card, step_header, section_badge,
    ACCENT, MED, DARK, SAND, GREEN,
)
from lib.mock_backend import list_bows, get_bow

st.set_page_config(page_title="Browse — GrainTrace",
                   page_icon="📚", layout="wide")
inject_global_css()

page_header(
    "Browse the bow database",
    "Every registered bow, its passport, and its photos.",
    section="SECTION · DATABASE",
)

bows = list_bows()

if not bows:
    st.info("No bows registered yet. Go to the **Enrol** page to add one.")
    st.stop()

# ===========================================================
# Filter + table
# ===========================================================
with card():
    section_badge("FILTERS & OVERVIEW")
    st.write("")

    col_search, col_school, col_count = st.columns([3, 2, 1])
    with col_search:
        q = st.text_input(
            "Search",
            placeholder="Search by maker, ID, owner, or notes…",
            label_visibility="collapsed",
        )
    with col_school:
        schools = sorted({b.school for b in bows if b.school})
        school_filter = st.selectbox(
            "School", ["All"] + schools,
            label_visibility="collapsed",
        )
    with col_count:
        st.metric("Total bows", len(bows))

    def matches(b) -> bool:
        if school_filter != "All" and b.school != school_filter:
            return False
        if q:
            hay = " ".join([b.bow_id, b.maker, b.owner or "",
                            b.notes or ""]).lower()
            if q.lower() not in hay:
                return False
        return True

    filtered = [b for b in bows if matches(b)]

    st.markdown(
        f"<p style='color:{MED}; font-size:13px; margin:6px 0'>"
        f"Showing {len(filtered)} of {len(bows)} bows</p>",
        unsafe_allow_html=True,
    )

    df = pd.DataFrame([
        {
            "Bow ID": b.bow_id,
            "Maker": b.maker,
            "Year": b.year or "—",
            "School": b.school or "—",
            "Owner": b.owner or "—",
            "Photos": len(b.photos),
            "Registered": b.registered_at[:10],
        }
        for b in filtered
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)

# ===========================================================
# Detail view
# ===========================================================
with card():
    section_badge("BOW DETAIL")
    st.write("")

    selected_id = st.selectbox(
        "Select a bow to view its passport",
        options=[b.bow_id for b in filtered],
        format_func=lambda bid: f"{bid} — {get_bow(bid).maker}",
    )

    if selected_id:
        b = get_bow(selected_id)
        if b is None:
            st.error("Bow not found.")
            st.stop()

        col_meta, col_photos = st.columns([1, 1.4], gap="large")

        with col_meta:
            st.markdown(
                f"<div style='font-family:Georgia,serif; font-size:32px; "
                f"font-weight:700; color:{DARK}; line-height:1.1'>"
                f"{b.bow_id}</div>"
                f"<div style='font-family:Georgia,serif; font-size:20px; "
                f"color:{ACCENT}; font-style:italic; margin-top:2px; "
                f"margin-bottom:18px'>{b.maker}</div>",
                unsafe_allow_html=True,
            )

            def kv(k, v):
                st.markdown(
                    f"<div style='display:flex; "
                    f"justify-content:space-between; padding:8px 0; "
                    f"border-bottom:1px solid {SAND}'>"
                    f"<span style='color:{MED}; font-size:11px; "
                    f"text-transform:uppercase; letter-spacing:0.5px; "
                    f"font-weight:700'>{k}</span>"
                    f"<span style='color:{DARK}; font-size:14px; "
                    f"font-weight:500'>{v or '—'}</span></div>",
                    unsafe_allow_html=True,
                )

            kv("Year", b.year)
            kv("School", b.school)
            kv("Owner", b.owner)
            kv("Photos", len(b.photos))
            kv("Registered", b.registered_at)
            kv("Model version", b.model_version)
            kv("Embedding length", len(b.embedding))

            if b.notes:
                st.markdown(
                    f"<div style='margin-top:14px'>"
                    f"<div style='color:{MED}; font-size:11px; "
                    f"text-transform:uppercase; letter-spacing:0.5px; "
                    f"font-weight:700; margin-bottom:6px'>Notes</div>"
                    f"<div style='background:#FBF5EC; "
                    f"border:1px solid {SAND}; border-radius:8px; "
                    f"padding:12px 14px; font-size:14px; color:{DARK}; "
                    f"line-height:1.55'>{b.notes}</div></div>",
                    unsafe_allow_html=True,
                )

        with col_photos:
            st.markdown("##### Photos")
            if not b.photos:
                st.caption("No photos on file.")
            else:
                n_cols = min(len(b.photos), 2)
                cols = st.columns(n_cols)
                for i, p in enumerate(b.photos):
                    with cols[i % n_cols]:
                        st.image(p, use_container_width=True,
                                 caption=f"Photo {i+1}")

            st.write("")
            st.markdown("##### Embedding preview")
            st.caption("First 32 dimensions of the bow's fingerprint vector.")
            st.bar_chart(b.embedding[:32], height=140)
