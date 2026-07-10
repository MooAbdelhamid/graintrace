import json
from typing import Dict, Optional

from fastapi import Form
from pydantic import BaseModel


class Bow(BaseModel):
    id: Optional[str] = (
        ""  # internally generated and required; hence default value "" for temporary assignment -- MAKE SURE THAT THIS IS ASSIGNED IN ANY CASE AS IT IS METADATA DB'S PRIMARY KEY
    )
    maker: str
    bow_kind: str | None = None
    brand: str | None = None
    school: str | None = None
    owner: str | None = None
    maker_assigned_id: str | None = None
    certificate_no: str | None = None
    stick_id_no: str | None = None
    proof_created_by: str | None = None
    place_of_issue: str | None = None
    date_of_issue: str | None = None
    wood_registration_date: str | None = None
    import_proof: str | None = None

    # The model stores a dictionary
    materials: Dict[str, str] | None = None

    notes: str | None = None

    @classmethod
    def as_form(
        cls,
        id: str | None = Form(None),
        maker: str = Form(...),
        bow_kind: str | None = Form(None),
        brand: str | None = Form(None),
        school: str | None = Form(None),
        owner: str | None = Form(None),
        maker_assigned_id: str | None = Form(None),
        certificate_no: str | None = Form(None),
        stick_id_no: str | None = Form(None),
        proof_created_by: str | None = Form(None),
        place_of_issue: str | None = Form(None),
        date_of_issue: str | None = Form(None),
        wood_registration_date: str | None = Form(None),
        import_proof: str | None = Form(None),
        # The HTTP form sends a string
        materials: str | None = Form(None),
        notes: str | None = Form(None),
    ):
        parsed_materials = json.loads(materials) if materials else None

        return cls(
            id=id,
            maker=maker,
            bow_kind=bow_kind,
            brand=brand,
            school=school,
            owner=owner,
            maker_assigned_id=maker_assigned_id,
            certificate_no=certificate_no,
            stick_id_no=stick_id_no,
            proof_created_by=proof_created_by,
            place_of_issue=place_of_issue,
            date_of_issue=date_of_issue,
            wood_registration_date=wood_registration_date,
            import_proof=import_proof,
            materials=parsed_materials,
            notes=notes,
        )
