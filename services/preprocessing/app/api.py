from fastapi import APIRouter, File, UploadFile
from fastapi.responses import Response
from transforms.popyperry import bytes_to_np, np_to_png, png_to_bytes, process_image

router = APIRouter()


@router.post("/preprocess")
async def pipeline(file: UploadFile = File(...)):
    content = await file.read()
    img = bytes_to_np(content)
    img = process_image(img)
    img = np_to_png(img)
    img = png_to_bytes(img)
    return Response(content=img, media_type=file.content_type)
