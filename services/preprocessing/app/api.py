from fastapi import APIRouter, File, UploadFile
from fastapi.responses import Response
from transforms.popyperry import image_process

router = APIRouter()


@router.post("/preprocess")
async def pipeline(file: UploadFile = File(...)):
    content = await file.read()
    output = image_process(content)
    return Response(content=output, media_type=file.content_type)
