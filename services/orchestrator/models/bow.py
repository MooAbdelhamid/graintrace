import json

from fastapi import Form
from pydantic import BaseModel


class Bow(BaseModel):
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
    materials: list[str] | None = None
    notes: str | None = None

    @classmethod
    def as_form(
        cls,
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
        materials: str | None = Form(None),
        notes: str | None = Form(None),
    ):
        return cls(
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
            materials=json.loads(materials) if materials else None,
            notes=notes,
        )
