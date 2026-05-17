from fastapi import APIRouter, File, Form, UploadFile
from schemas import VerifyResponse

router = APIRouter


@router.post("/verify", response_model=VerifyResponse)
async def verify(
    image: UploadFile = File(...),
    top_k: int = Form(5),
    threshold: float = Form(0.85),
):
    return {
        "filename": image.filename,
        "top_k": top_k,
        "threshold": threshold,
    }
