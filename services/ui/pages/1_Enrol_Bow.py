"""Enrol a new bow. Sends the passport + image to the orchestrator."""

import streamlit as st
from lib import api_client
from lib.schemas import Bow

st.set_page_config(page_title="Enrol a bow", layout="wide")
st.title("Enrol a bow")
st.caption("Fill in the passport, upload one head photo, submit.")

# ---------------------------------------------------------------------------
# Passport form
# ---------------------------------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    maker = st.text_input("Maker *", placeholder="e.g. Eugène Sartory")
    bow_kind = st.text_input("Kind of bow", placeholder="e.g. Violin bow")
    brand = st.text_input("Brand", placeholder="Punch on the bow, e.g. E. SARTORY")
    school = st.selectbox(
        "School / origin",
        ["", "French", "English", "German", "American", "Italian", "Other"],
    )
    owner = st.text_input("Owner")

    st.divider()
    st.caption("External identifiers (optional)")
    maker_assigned_id = st.text_input("Maker's own catalog number")
    certificate_no = st.text_input("Certificate No.")
    stick_id_no = st.text_input("Stick ID No.")

with col2:
    proof_created_by = st.text_input(
        "Proof created by", placeholder="Name and address of the issuer"
    )
    place_of_issue = st.text_input("Place of issue")
    date_of_issue = st.text_input("Date of issue", placeholder="DD-MM-YYYY")
    wood_registration_date = st.text_input(
        "Wood registration date", placeholder="DD-MM-YYYY"
    )
    import_proof = st.text_input("Import proof")

    st.divider()
    notes = st.text_area(
        "Notes / specifics",
        placeholder="Condition, repair history, distinguishing marks…",
        height=140,
    )

# ---------------------------------------------------------------------------
# Materials
# ---------------------------------------------------------------------------

st.subheader("Materials")
st.caption("Fill in whichever parts the passport lists — blank fields are ignored.")

material_keys = [
    "stick",
    "faceplate",
    "mounting",
    "lapping",
    "frog",
    "slide",
    "eye",
    "metal",
    "hair",
]

placeholders = {
    "stick": "Pernambuco",
    "faceplate": "Ivory",
    "mounting": "Silver",
    "lapping": "Bovine leather",
    "frog": "Ebony",
    "slide": "Mother-of-pearl",
    "eye": "Abalone",
    "metal": "Nickel-silver",
    "hair": "Horse hair",
}

materials: dict[str, str] = {}
mcols = st.columns(3)
for i, key in enumerate(material_keys):
    with mcols[i % 3]:
        v = st.text_input(key.capitalize(), placeholder=placeholders[key])
        if v.strip():
            materials[key] = v.strip()

# ---------------------------------------------------------------------------
# Photo + submit
# ---------------------------------------------------------------------------

st.subheader("Photo")
photo = st.file_uploader(
    "Bow head photo",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed",
)

if photo is not None:
    st.image(photo, use_container_width=False, width=400)

st.write("")
submit = st.button(
    "Register bow",
    type="primary",
    disabled=not (maker and photo),
)

if submit:
    try:
        bow = Bow(
            maker=maker.strip(),
            bow_kind=bow_kind.strip() or None,
            brand=brand.strip() or None,
            school=school or None,
            owner=owner.strip() or None,
            maker_assigned_id=maker_assigned_id.strip() or None,
            certificate_no=certificate_no.strip() or None,
            stick_id_no=stick_id_no.strip() or None,
            proof_created_by=proof_created_by.strip() or None,
            place_of_issue=place_of_issue.strip() or None,
            date_of_issue=date_of_issue.strip() or None,
            wood_registration_date=wood_registration_date.strip() or None,
            import_proof=import_proof.strip() or None,
            materials=materials,
            notes=notes.strip(),
        )

        with st.spinner("Registering..."):
            result = api_client.register(bow, photo.getvalue(), filename=photo.name)

        st.success(f"Registered: **{result.get('bow_id', '(no id in response)')}**")

        st.json(result)

    except Exception as e:
        st.error(f"Registration failed: {type(e).__name__}: {e}")
