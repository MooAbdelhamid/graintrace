import numpy as np
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import Response

router = APIRouter()


@router.post("/infer")
async def pipeline(file: UploadFile = File(...)):

    content = await file.read()

    embedding = np.random.rand(512).astype(np.float32)

    raw_bytes = embedding.tobytes()

    return Response(content=raw_bytes)
