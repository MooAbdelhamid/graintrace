import base64

from clients.model import model_call
from clients.preprocessing import preprocessing_call
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/verify")
async def verify(file: UploadFile = File(...)):
    """
    input: Bytes
    output:
    """
    content = await file.read()  # bytes

    data = {"filename": file.filename, "type": file.content_type}

    img = preprocessing_call(content, data)  # bytes

    data = {"filename": file.filename, "type": file.content_type}

    result = model_call(img, data)  # bytes

    response = {
        "image": base64.b64encode(img).decode("utf-8"),
        "embedding": base64.b64encode(result).decode("utf-8"),
        "embedding_shape": [512],
        "dtype": "float32",
        "meta": data,
    }

    return JSONResponse(response)
