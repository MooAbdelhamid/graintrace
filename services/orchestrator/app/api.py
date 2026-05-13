from fastapi import APIRouter
from schemas import VerifyRequest, VerifyResponse

router = APIRouter


@router.post("/verify", response_model=VerifyResponse)
def verify(request: VerifyRequest):
    pass
