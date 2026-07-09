import datetime
from datetime import date
from typing import Optional, Union  # , List

from pydantic import BaseModel, Field


class Bow(BaseModel):
    id: str
    maker_assigned_id: Optional[str] = None
    certificate_no: Optional[str] = None
    stick_id_no: Optional[str] = None
    maker: str = ""
    bow_kind: Optional[str] = None
    brand: Optional[str] = None
    school: Optional[str] = None
    owner: Optional[str] = None
    proof_created_by: Optional[str] = None
    place_of_issue: Optional[str] = None
    # date_of_issue: Optional[str] = None
    date_of_issue: Optional[Union[str, date]] = None
    # wood_registration_date: Optional[str] = None
    wood_registration_date: Optional[Union[str, date]] = None
    import_proof: Optional[str] = None
    notes: str = ""
    # materials: Optional[Dict] = Field(default_factory=dict)
    # registered_at: Optional[datetime] = Field(default_factory=datetime.now(datetime.timezone.utc))
    registered_at: Optional[datetime.datetime] = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    # updated_at: Optional[datetime] = Field(default_factory=datetime.now(datetime.timezone.utc))
    updated_at: Optional[datetime.datetime] = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    # photos: Optional[List] = Field(default_factory=list) # maybe read the image names and save them here?

    # def to_dict(self):
    #     """Convert the object to a dictionary for database insertion."""
    #     # Pydantic models have a built-in .dict() method
    #     # You can customize it if needed, but usually .dict() suffices
    #     return self.model_dump(exclude={"photos"})

    @classmethod
    def as_form(
        cls,
        id: str,
        maker_assigned_id: Optional[str] = None,
        certificate_no: Optional[str] = None,
        stick_id_no: Optional[str] = None,
        maker: str = "",
        bow_kind: Optional[str] = None,
        brand: Optional[str] = None,
        school: Optional[str] = None,
        owner: Optional[str] = None,
        proof_created_by: Optional[str] = None,
        place_of_issue: Optional[str] = None,
        date_of_issue: Optional[Union[str, date]] = None,
        wood_registration_date: Optional[Union[str, date]] = None,
        import_proof: Optional[str] = None,
        notes: str = "",
        # materials: Optional[Dict] = None,
        registered_at: Optional[datetime.datetime] = None,
        updated_at: Optional[datetime.datetime] = None,
    ):
        return cls(
            id=id,
            maker_assigned_id=maker_assigned_id,
            certificate_no=certificate_no,
            stick_id_no=stick_id_no,
            maker=maker,
            bow_kind=bow_kind,
            brand=brand,
            school=school,
            owner=owner,
            proof_created_by=proof_created_by,
            place_of_issue=place_of_issue,
            date_of_issue=date_of_issue,
            wood_registration_date=wood_registration_date,
            import_proof=import_proof,
            notes=notes,
            # materials=materials or {},
            registered_at=registered_at,
            updated_at=updated_at,
        )
