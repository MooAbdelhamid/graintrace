"""Identification flow — upload a query photo and find the closest bow."""
import streamlit as st

from lib.style import (
    inject_global_css, page_header, card, step_header, section_badge,
    reject_box,
    ACCENT, MED, DARK, GREEN, SAND, WHITE,
)
from lib.mock_backend import query_bow
from lib.photo_check import preflight, status_color, status_emoji

st.set_page_config(page_title="Identify a bow — GrainTrace",
                   page_icon="🔍", layout="wide")
inject_global_css()

page_header(
    "Identify a bow",
    "Upload one or more head photos of an unknown bow — we'll show the closest matches in the database.",
    section="SECTION · IDENTIFY",
)

# ===========================================================
# STEP 1 — Upload + preflight
# ===========================================================
go = False
photo_bytes: list[bytes] = []

with card():
    step_header(1, "Upload query photo(s)",
                "Side and front views work best. Each photo is checked against the rejection rules first.")

    uploaded = st.file_uploader(
        "Upload query images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    any_failed = False
    any_passed = False

    if uploaded:
        for f in uploaded:
            photo_bytes.append(f.getvalue())

        st.write("")
        cols = st.columns(min(len(uploaded), 3))
        for i, f in enumerate(uploaded):
            with cols[i % len(cols)]:
                report = preflight(f.getvalue())
                badge_color = status_color(report.overall)
                badge_text = {"pass": "OK",
                              "warn": "Marginal",
                              "fail": "Rejected"}[report.overall]

                st.image(f.getvalue(), use_container_width=True)
                st.markdown(
                    f"<div style='display:flex; align-items:center; "
                    f"justify-content:space-between; margin-top:6px'>"
                    f"<span style='font-size:13px; color:{MED}; "
                    f"overflow:hidden; text-overflow:ellipsis; "
                    f"white-space:nowrap; max-width:60%'>{f.name}</span>"
                    f"<span style='background:{badge_color}; color:white; "
                    f"padding:3px 11px; border-radius:999px; font-size:11px; "
                    f"font-weight:700; letter-spacing:0.5px'>"
                    f"{badge_text.upper()}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

                fails = [c for c in report.checks if c.status == "fail"]
                if fails:
                    any_failed = True
                    reasons = "<br>".join(
                        f"<b>{c.label}:</b> {c.detail}" for c in fails
                    )
                    reject_box(f"<b>Why rejected</b><br>{reasons}", "fail")
                else:
                    any_passed = True
    else:
        st.info("Upload a photo of the bow head to start.")

    can_query = bool(uploaded) and any_passed and not any_failed

    st.write("")
    if uploaded and any_failed:
        st.error(
            "**Can't run a query — one or more photos were rejected.**\n\n"
            "Remove or replace them, then try again. The red panels above "
            "each rejected photo list the exact reason."
        )

    go = st.button("🔍  Find matches", type="primary",
                   disabled=not can_query, use_container_width=False)

# ===========================================================
# STEP 2 — Results
# ===========================================================
if go and photo_bytes:
    with st.spinner("Computing embedding and searching the database…"):
        results = query_bow(photo_bytes, top_k=3)

    if not results:
        st.warning("Database is empty — nothing to match against.")
    else:
        top = results[0]

        # ---- Verdict card ----
        if top.confidence == "high":
            verdict_color = GREEN
            verdict_bg = "#E1F0D5"
            verdict_icon = "✓"
            verdict_text = f"Match found — {top.passport.bow_id}"
            verdict_sub = "High confidence in this match."
        elif top.confidence == "medium":
            verdict_color = ACCENT
            verdict_bg = "#FBE9D6"
            verdict_icon = "?"
            verdict_text = f"Possible match — {top.passport.bow_id}"
            verdict_sub = "Moderate confidence — please verify visually."
        else:
            verdict_color = "#842029"
            verdict_bg = "#F8D7DA"
            verdict_icon = "✕"
            verdict_text = "No confident match"
            verdict_sub = "The query may not be in the database yet."

        with card():
            step_header(2, "Top match")
            st.markdown(
                f"<div style='background:{verdict_bg}; "
                f"border-left:6px solid {verdict_color}; border-radius:10px; "
                f"padding:18px 22px; display:flex; align-items:center; gap:18px'>"
                f"<div style='font-size:42px; font-weight:700; "
                f"color:{verdict_color}; line-height:1'>{verdict_icon}</div>"
                f"<div style='flex:1'>"
                f"<div style='font-family:Georgia,serif; font-size:24px; "
                f"font-weight:700; color:{verdict_color}'>{verdict_text}</div>"
                f"<div style='color:{MED}; font-size:14px; margin-top:4px'>"
                f"{verdict_sub}</div>"
                f"</div>"
                f"<div style='text-align:right'>"
                f"<div style='font-family:Georgia,serif; font-size:32px; "
                f"font-weight:700; color:{verdict_color}'>"
                f"{top.score:.0%}</div>"
                f"<div style='font-size:11px; color:{MED}; "
                f"text-transform:uppercase; letter-spacing:0.5px; "
                f"font-weight:700'>similarity</div>"
                f"</div></div>",
                unsafe_allow_html=True,
            )

        # ---- Top-3 candidate list ----
        with card():
            step_header(3, "Top 3 candidates",
                        "Sorted by similarity. Confirm the right one or "
                        "register a new bow.")

            for r in results:
                bar_color = {"high": GREEN, "medium": ACCENT,
                             "low": "#842029"}[r.confidence]
                conf_bg = {"high": "#E1F0D5", "medium": "#FBE9D6",
                           "low": "#F8D7DA"}[r.confidence]

                with st.container():
                    cols = st.columns([1, 1.3, 3, 1.4])

                    # 1. Score badge
                    with cols[0]:
                        st.markdown(
                            f"<div style='background:{conf_bg}; "
                            f"border-radius:10px; padding:14px; "
                            f"text-align:center'>"
                            f"<div style='font-family:Georgia,serif; "
                            f"font-size:28px; font-weight:700; "
                            f"color:{bar_color}; line-height:1'>"
                            f"{r.score:.0%}</div>"
                            f"<div style='font-size:10px; "
                            f"text-transform:uppercase; letter-spacing:0.5px; "
                            f"color:{MED}; font-weight:700; "
                            f"margin-top:4px'>{r.confidence}</div>"
                            f"</div>",
                            unsafe_allow_html=True,
                        )

                    # 2. Bow photo
                    with cols[1]:
                        if r.passport.photos:
                            st.image(r.passport.photos[0],
                                     use_container_width=True)
                        else:
                            st.markdown(
                                f"<div style='background:{SAND}; height:90px; "
                                f"border-radius:6px; display:flex; "
                                f"align-items:center; justify-content:center; "
                                f"color:{MED}; font-size:12px'>"
                                f"(no photo)</div>",
                                unsafe_allow_html=True,
                            )

                    # 3. Bow info
                    with cols[2]:
                        st.markdown(
                            f"<div style='font-family:Georgia,serif; "
                            f"font-size:17px; font-weight:700; color:{DARK}'>"
                            f"{r.passport.bow_id}  ·  {r.passport.maker}"
                            f"</div>",
                            unsafe_allow_html=True,
                        )
                        info_bits = []
                        if r.passport.year:
                            info_bits.append(r.passport.year)
                        if r.passport.school:
                            info_bits.append(r.passport.school)
                        if r.passport.owner:
                            info_bits.append(f"owner: {r.passport.owner}")
                        if info_bits:
                            st.markdown(
                                f"<div style='color:{MED}; font-size:13px; "
                                f"margin-top:2px'>"
                                f"{'  ·  '.join(info_bits)}</div>",
                                unsafe_allow_html=True,
                            )
                        if r.passport.notes:
                            st.markdown(
                                f"<div style='color:{MED}; font-size:12.5px; "
                                f"margin-top:6px; line-height:1.5'>"
                                f"{r.passport.notes[:140]}</div>",
                                unsafe_allow_html=True,
                            )

                    # 4. Confirm button
                    with cols[3]:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("This is the bow",
                                     key=f"confirm-{r.bow_id}",
                                     type="secondary",
                                     use_container_width=True):
                            st.success(
                                f"Confirmed match for {r.bow_id}. "
                                f"(In the real system, this writes a query "
                                f"event to the ledger.)"
                            )

                    st.markdown(
                        f"<hr style='margin:14px 0; border:none; "
                        f"border-top:1px solid {SAND}'>",
                        unsafe_allow_html=True,
                    )

        # ---- Fallback enrolment ----
        if top.confidence != "high":
            with card():
                st.markdown(
                    f"<div style='display:flex; gap:14px; align-items:center'>"
                    f"<div style='font-size:32px'>+</div>"
                    f"<div style='flex:1'>"
                    f"<b style='font-family:Georgia,serif; font-size:17px'>"
                    f"No confident match?</b><br>"
                    f"<span style='color:{MED}; font-size:14px'>"
                    f"If this bow isn't in our database yet, register it now."
                    f"</span></div></div>",
                    unsafe_allow_html=True,
                )
                st.write("")
                if st.button("→ Enrol this as a new bow", type="primary"):
                    st.switch_page("pages/1_Enrol_Bow.py")
