from fastapi import APIRouter, File, UploadFile
from fastapi.responses import Response

router = APIRouter()


@router.post("/infer")
async def pipeline(file: UploadFile = File(...)):
    content = await file.read()

    return Response(content=content, media_type=file.content_type)
