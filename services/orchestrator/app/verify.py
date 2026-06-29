import json

from clients.metadata import meta_search
from clients.model import model_call
from clients.preprocessing import preprocessing_call
from clients.retrieval import retrieval_search
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/verify", tags=["verify"])


@router.post("/")
async def verify(file: UploadFile = File(...)):

    content = await file.read()  # bytes

    data = {"filename": file.filename, "type": file.content_type}

    img = preprocessing_call(content, data)  # bytes

    print(type(img))

    embedding_bytes = model_call(img, data)  # bytes

    print(type(embedding_bytes))

    embeddings = json.loads(embedding_bytes.decode("utf-8"))  # dict

    print(type(embeddings))

    embeddings = embeddings["embeddings"]  # list

    print(type(embeddings))

    result = retrieval_search(embeddings)  # dict

    print(type(result))

    print(result)

    matches = []

    for item in result["results"]:
        bow_id = item["bow_id"]
        score = item["score"]

        metadata = meta_search(bow_id)

        matches.append({"bow_id": bow_id, "score": score, **metadata})

    response = {"status": "success", "matches": matches}

    return JSONResponse(response)
