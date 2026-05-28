"""Enrolment flow — register a new bow."""
import streamlit as st

from lib.style import (
    inject_global_css, page_header, card, step_header, section_badge,
    reject_box, status_badge,
    ACCENT, MED, DARK, GREEN, SAND,
)
from lib.mock_backend import enroll_bow, next_bow_id
from lib.photo_check import preflight, status_color, status_emoji

st.set_page_config(page_title="Enrol a bow — GrainTrace",
                   page_icon="📝", layout="wide")
inject_global_css()

page_header(
    "Enrol a new bow",
    "Three steps: passport details, photo upload with quality check, review and confirm.",
    section="SECTION · ENROL",
)

# ===========================================================
# STEP 1 — Passport details
# ===========================================================
with card():
    step_header(1, "Passport details", "Bow identity and provenance")
    col_a, col_b = st.columns(2)
    with col_a:
        bow_id = st.text_input(
            "Bow ID", value=next_bow_id(),
            help="A unique identifier. Auto-generated; override if you "
                 "have an existing scheme.",
        )
        maker = st.text_input("Maker", placeholder="e.g. Eugène Sartory")
        year = st.text_input("Year (approx.)", placeholder="e.g. 1925")
    with col_b:
        school = st.selectbox(
            "School / origin",
            ["", "French", "English", "German", "American",
             "Italian", "Other / unknown"],
        )
        owner = st.text_input("Current owner / holder",
                              placeholder="Optional")
        st.text_input("",  # spacer to align with left column
                      placeholder="", label_visibility="collapsed",
                      disabled=True, key="_spacer")
    notes = st.text_area("Notes",
                         placeholder="Condition, repair history, "
                                     "distinguishing marks…",
                         height=80)

# ===========================================================
# STEP 2 — Photo upload + preflight
# ===========================================================
with card():
    step_header(2, "Head photos",
                "Upload at least two views of the head — side and front.")
    st.caption(
        "Every photo is checked against the rejection rules: "
        "**resolution ≥ 10 MP**, **sharp focus**, **head fully visible**, "
        "**no heavy glare**."
    )

    uploaded = st.file_uploader(
        "Upload images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    photo_bytes: list[bytes] = []
    photo_reports = []   # list of (filename, PreflightReport)

    if uploaded:
        for f in uploaded:
            photo_bytes.append(f.getvalue())
            photo_reports.append((f.name, preflight(f.getvalue())))

        st.write("")
        cols = st.columns(min(len(uploaded), 3))
        for i, (f, (_, report)) in enumerate(zip(uploaded, photo_reports)):
            with cols[i % len(cols)]:
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
                warns = [c for c in report.checks if c.status == "warn"]

                if fails:
                    reasons = "<br>".join(
                        f"<b>{c.label}:</b> {c.detail}" for c in fails
                    )
                    reject_box(f"<b>Why rejected</b><br>{reasons}", "fail")
                elif warns:
                    reasons = "<br>".join(
                        f"<b>{c.label}:</b> {c.detail}" for c in warns
                    )
                    reject_box(f"<b>Marginal — review</b><br>{reasons}",
                               "warn")

                with st.expander("Full quality report", expanded=False):
                    for chk in report.checks:
                        color = status_color(chk.status)
                        st.markdown(
                            f"<div style='display:flex; "
                            f"justify-content:space-between; "
                            f"border-bottom:1px solid {SAND}; "
                            f"padding:6px 0; font-size:13px'>"
                            f"<span><span style='color:{color}; "
                            f"font-weight:700'>{status_emoji(chk.status)}"
                            f"</span>  {chk.label}</span>"
                            f"<span style='color:{MED}'>"
                            f"{chk.detail}</span></div>",
                            unsafe_allow_html=True,
                        )
    else:
        st.info("No photos uploaded yet. Drop one or more JPEGs above.")

# ===========================================================
# STEP 3 — Review & confirm
# ===========================================================
with card():
    step_header(3, "Review & confirm")

    rejected = [(name, [c for c in rep.checks if c.status == "fail"])
                for name, rep in photo_reports if rep.overall == "fail"]
    accepted = [name for name, rep in photo_reports
                if rep.overall != "fail"]

    blockers = []
    warnings = []
    if not maker:
        blockers.append("Maker is empty — required ID information for the session.")
    if not uploaded:
        blockers.append("At least one photo is required.")
    elif len(accepted) < 2:
        warnings.append(
            f"Only {len(accepted)} photo(s) passed — 2 or more (side + front) recommended."
        )
    if rejected:
        blockers.append(
            f"{len(rejected)} photo(s) failed the quality check — see below."
        )

    if blockers:
        st.error(
            "**Can't submit yet — please fix:**\n\n"
            + "\n".join(f"- {b}" for b in blockers)
        )
    elif warnings:
        st.warning("\n".join(f"- {w}" for w in warnings))
    elif uploaded and accepted:
        st.success(
            f"**Ready to register** — {len(accepted)} photo(s) accepted "
            f"for **{maker}**."
        )

    # Per-photo rejection summary
    if rejected:
        st.markdown("##### Per-photo rejection summary")
        for name, fails in rejected:
            with st.container():
                st.markdown(
                    f"<div style='background:#FFF7F7; border:1px solid "
                    f"#F0CCCF; border-radius:8px; padding:10px 14px; "
                    f"margin-bottom:8px'>"
                    f"<b style='color:#842029'>📷 {name}</b>"
                    + "".join(
                        f"<div style='margin-left:18px; color:#842029; "
                        f"font-size:13px; margin-top:3px'>"
                        f"• <b>{c.label}:</b> {c.detail}</div>"
                        for c in fails
                    )
                    + "</div>",
                    unsafe_allow_html=True,
                )

    st.write("")
    submit = st.button("✓  Register bow", type="primary",
                       disabled=bool(blockers),
                       use_container_width=False)

    if submit:
        fields = {
            "bow_id": bow_id, "maker": maker, "year": year or None,
            "school": school or None, "owner": owner or None, "notes": notes,
        }
        keep = [
            pb for pb, (_, rep) in zip(photo_bytes, photo_reports)
            if rep.overall != "fail"
        ]
        new_id = enroll_bow(fields, keep)
        st.success(f"✓ Registered **{new_id}** — {maker}")
        st.balloons()
        st.markdown(
            f"<div style='background:#E1F0D5; border-radius:10px; "
            f"padding:14px 16px; border-left:4px solid {GREEN}; "
            f"margin-top:10px'>"
            f"<b>{new_id}</b> is now in the database with {len(keep)} photo(s) "
            f"and a 256-dimensional embedding.<br>"
            f"You can now <i>identify</i> any future photo of this bow "
            f"against it.</div>",
            unsafe_allow_html=True,
        )
        st.write("")
        col_a, col_b, _ = st.columns([1, 1, 2])
        if col_a.button("Enrol another bow"):
            st.rerun()
        if col_b.button("Browse database →"):
            st.switch_page("pages/3_Browse_Database.py")
