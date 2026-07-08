"""Pydantic model built from the enrolment form and sent to the orchestrator."""

from typing import Dict, Optional

from pydantic import BaseModel


class Bow(BaseModel):
    # required
    maker: str

    # identity
    bow_kind: Optional[str] = None
    brand: Optional[str] = None
    school: Optional[str] = None
    owner: Optional[str] = None

    # external IDs
    maker_assigned_id: Optional[str] = None
    certificate_no: Optional[str] = None
    stick_id_no: Optional[str] = None

    # provenance
    proof_created_by: Optional[str] = None
    place_of_issue: Optional[str] = None
    date_of_issue: Optional[str] = None  # DD-MM-YYYY
    wood_registration_date: Optional[str] = None  # DD-MM-YYYY
    import_proof: Optional[str] = None

    # materials + free text
    materials: Dict[str, str] = {}
    notes: str = ""
