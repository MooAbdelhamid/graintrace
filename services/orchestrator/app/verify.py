import json

from clients.model import model_call
from clients.preprocessing import preprocessing_call
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/verify", tags=["verify"])


@router.post("/")
async def verify(file: UploadFile = File(...)):

    content = await file.read()

    data = {"filename": file.filename, "type": file.content_type}

    img = preprocessing_call(content, data)

    embedding_bytes = model_call(img, data)

    embeddings = json.loads(embedding_bytes.decode("utf-8"))

    embeddings = embeddings["embeddings"]

    print(type(embeddings))

    response = {
        "embedding": embeddings,
        "embedding_shape": [256],
        "dtype": "float32",
        "meta": data,
    }

    return JSONResponse(response)
