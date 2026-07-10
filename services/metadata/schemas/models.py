import datetime
import json
from datetime import date
from typing import Dict, Optional, Union  # , List

from fastapi import Form
from pydantic import BaseModel, Field


class Bow(BaseModel):
    # required
    maker: str

    # characteristics
    bow_kind: Optional[str] = None
    brand: Optional[str] = None
    school: Optional[str] = None
    owner: Optional[str] = None

    # IDs
    id: Optional[str] = (
        ""  # internally generated and required; hence default value "" for temporary assignment -- MAKE SURE THAT THIS IS ASSIGNED IN ANY CASE AS IT IS METADATA DB'S PRIMARY KEY
    )
    maker_assigned_id: Optional[str] = None
    certificate_no: Optional[str] = None
    stick_id_no: Optional[str] = None

    # provenance
    proof_created_by: Optional[str] = None
    place_of_issue: Optional[str] = None
    date_of_issue: Optional[Union[str, date]] = (
        None  # UI should make sure that this is passed as a valid date format
    )
    wood_registration_date: Optional[Union[str, date]] = (
        None  # UI should make sure that this is passed as a valid date format
    )
    import_proof: Optional[str] = None

    # materials + free text
    materials: Optional[Dict] = None
    notes: Optional[str] = None
    # image_metadata: Optional[List] = Field(default_factory=list) # maybe read the image names and save them here?

    # timestamps
    registered_at: Optional[datetime.datetime] = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: Optional[datetime.datetime] = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )  # add update option?

    @classmethod
    def as_form(
        cls,
        id: Optional[str] = Form(None),
        maker: str = Form(...),
        bow_kind: Optional[str] = Form(None),
        brand: Optional[str] = Form(None),
        school: Optional[str] = Form(None),
        owner: Optional[str] = Form(None),
        maker_assigned_id: Optional[str] = Form(None),
        certificate_no: Optional[str] = Form(None),
        stick_id_no: Optional[str] = Form(None),
        proof_created_by: Optional[str] = Form(None),
        place_of_issue: Optional[str] = Form(None),
        date_of_issue: Optional[str] = Form(None),  # change?
        wood_registration_date: Optional[str] = Form(None),  # change?
        import_proof: Optional[str] = Form(None),
        materials: Optional[str] = Form(None),  # change?
        notes: Optional[str] = Form(None),
        # registered_at: Optional[str] = Form(None),
        # updated_at: Optional[str] = Form(None),
    ):
        # parse materials JSON string if provided
        parsed_materials = json.loads(materials) if materials else None

        # if UI does not take care of it, make sure to parse date strings to date objects

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
            # registered_at=registered_at,
            # updated_at=updated_at,
        )
