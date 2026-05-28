"""Shared style helpers — keeps the look-and-feel consistent across pages."""
from contextlib import contextmanager

import streamlit as st

# Palette from the GrainTrace deck
DARK = "#2D3748"
MED = "#4A5568"
SOFT = "#718096"
ACCENT = "#A8633D"
LIGHT_ACCENT = "#C6896A"
GREEN = "#38761D"
LIGHT_GREEN = "#E1F0D5"
CREAM = "#FAF6F1"
SAND = "#EBE0D2"
WHITE = "#FFFFFF"


def inject_global_css():
    """Inject custom CSS that pushes the look beyond default Streamlit."""
    st.markdown(
        f"""
        <style>
          /* Serif treatment for all headings */
          h1, h2, h3, h4, h5, h6,
          .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
          .stMarkdown h4, .stMarkdown h5 {{
              font-family: Georgia, 'Times New Roman', serif !important;
              color: {DARK};
              font-weight: 700;
              letter-spacing: -0.01em;
          }}

          /* Tighter, more refined h1 */
          h1 {{ font-size: 38px !important; line-height: 1.2 !important;
                margin-bottom: 4px !important; }}

          /* Section dividers — accent colour */
          hr {{ border: none; border-top: 1px solid {SAND}; margin: 1.2em 0; }}

          /* Streamlit's native bordered container — soften it */
          div[data-testid="stVerticalBlockBorderWrapper"] {{
              background: {WHITE};
              border: 1px solid {SAND} !important;
              border-radius: 14px !important;
              padding: 26px 30px !important;
              box-shadow: 0 1px 3px rgba(45, 55, 72, 0.04);
              margin-bottom: 22px;
          }}

          /* Section number badge */
          .step-badge {{
              display: inline-flex;
              align-items: center;
              justify-content: center;
              width: 30px; height: 30px;
              border-radius: 999px;
              background: {ACCENT};
              color: white;
              font-family: Georgia, serif;
              font-weight: 700;
              font-size: 15px;
              margin-right: 12px;
              vertical-align: middle;
          }}
          .step-title {{
              font-family: Georgia, serif;
              font-size: 22px;
              font-weight: 700;
              color: {DARK};
              vertical-align: middle;
          }}
          .step-subtitle {{
              color: {MED};
              font-size: 14px;
              margin-top: 6px;
              margin-left: 42px;
          }}

          /* Small-caps section label */
          .small-caption {{
              font-size: 11px; color: {MED};
              letter-spacing: 0.6px;
              text-transform: uppercase;
              font-weight: 700;
          }}

          /* Status badges (pass / warn / fail) */
          .badge {{
              display: inline-block;
              padding: 3px 11px;
              border-radius: 999px;
              font-size: 11px;
              font-weight: 700;
              letter-spacing: 0.5px;
              text-transform: uppercase;
          }}
          .badge-pass {{ background: {LIGHT_GREEN}; color: {GREEN}; }}
          .badge-warn {{ background: #FBE9D6; color: {ACCENT}; }}
          .badge-fail {{ background: #F8D7DA; color: #842029; }}

          /* Reject reasons box */
          .reject-box {{
              background: #F8D7DA;
              border-left: 4px solid #842029;
              border-radius: 8px;
              padding: 10px 14px;
              margin-top: 8px;
              font-size: 12.5px;
              color: #842029;
              line-height: 1.55;
          }}
          .warn-box {{
              background: #FBE9D6;
              border-left: 4px solid {ACCENT};
              border-radius: 8px;
              padding: 10px 14px;
              margin-top: 8px;
              font-size: 12.5px;
              color: {ACCENT};
              line-height: 1.55;
          }}

          /* Photo card frame around uploaded images */
          .photo-frame {{
              border: 1px solid {SAND};
              border-radius: 10px;
              padding: 8px;
              background: {WHITE};
          }}

          /* Inputs feel less cramped */
          .stTextInput, .stSelectbox, .stTextArea {{
              margin-bottom: 6px !important;
          }}

          /* Buttons — slight refinement */
          .stButton > button {{
              border-radius: 8px !important;
              font-weight: 600 !important;
              padding: 9px 18px !important;
          }}

          /* Metric polish */
          [data-testid="stMetric"] {{
              background: {WHITE};
              border: 1px solid {SAND};
              border-radius: 12px;
              padding: 14px 18px;
          }}

          /* File uploader — softer border */
          [data-testid="stFileUploaderDropzone"] {{
              border: 2px dashed {SAND} !important;
              background: {CREAM} !important;
              border-radius: 12px !important;
          }}

          /* Sidebar */
          [data-testid="stSidebar"] {{
              background: {WHITE};
              border-right: 1px solid {SAND};
          }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_badge(label: str):
    st.markdown(f'<span class="small-caption">{label}</span>',
                unsafe_allow_html=True)


def status_badge(label: str, status: str = "pass"):
    cls = f"badge-{status}"
    st.markdown(f'<span class="badge {cls}">{label}</span>',
                unsafe_allow_html=True)


def step_header(number: int, title: str, subtitle: str = ""):
    """Render a numbered step heading inside a section card."""
    html = (
        f"<div><span class='step-badge'>{number}</span>"
        f"<span class='step-title'>{title}</span></div>"
    )
    if subtitle:
        html += f"<div class='step-subtitle'>{subtitle}</div>"
    st.markdown(html, unsafe_allow_html=True)
    st.write("")  # small breathing room


def page_header(title: str, subtitle: str = "", section: str = ""):
    if section:
        section_badge(section)
    st.markdown(f"# {title}")
    if subtitle:
        st.markdown(
            f"<p style='color:{MED}; font-style:italic; font-size:16px; "
            f"margin-top:-4px; margin-bottom:24px'>{subtitle}</p>",
            unsafe_allow_html=True,
        )


@contextmanager
def card():
    """Wrap a block of content in a section card.

    Usage:
        with card():
            step_header(1, "Passport details")
            ...form fields...
    """
    with st.container(border=True):
        yield


def reject_box(reasons_html: str, kind: str = "fail"):
    """Render the rejection reasons panel. kind in {'fail', 'warn'}."""
    cls = "reject-box" if kind == "fail" else "warn-box"
    st.markdown(f'<div class="{cls}">{reasons_html}</div>',
                unsafe_allow_html=True)
