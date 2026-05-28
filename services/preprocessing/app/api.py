from fastapi import APIRouter, File, UploadFile
from fastapi.responses import Response
from pipeline.image_pipeline import ImagePipeline
from utils.utils import decode_image, encode_image

router = APIRouter()
imagepipeline = ImagePipeline()


@router.post("/preprocess")
async def pipeline(file: UploadFile = File(...)):
    content = await file.read()

    result = imagepipeline.run(decode_image(content))

    return Response(content=encode_image(result), media_type=file.content_type)
