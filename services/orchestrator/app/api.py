from clients.model import model_call
from clients.preprocessing import preprocessing_call
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import Response

router = APIRouter()


@router.post("/verify")
async def verify(file: UploadFile = File(...)):
    content = await file.read()
    data = {"filename": file.filename, "type": file.content_type}
    img = preprocessing_call(content, data)
    result = model_call(img, file.filename, file.content_type)
    return Response(content=result, media_type=file.content_type)
