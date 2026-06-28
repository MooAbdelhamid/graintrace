import json
import uuid

from clients.model import model_call
from clients.preprocessing import preprocessing_call
from clients.retrieval import retrieval_store
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/register", tags=["register"])


def generate_bow_id() -> str:
    # orchestrator assigns bow_id in format BOW-XXXXXX
    return f"BOW-{uuid.uuid4().hex[:6].upper()}"


@router.post("/")
async def register(
    file: UploadFile = File(...),
    maker: str = Form(...),
    bow_kind: str | None = Form(None),
    owner: str | None = Form(None),
):
    # input:  JPEG image + bow passport fields as form fields
    # output: EnrollResponse with bow_id, embedding_dim, status, passport
    content = await file.read()
    print(type(content))

    data = {"filename": file.filename, "type": file.content_type}

    bow_id = generate_bow_id()  # orchestrator assigns the system ID

    img = preprocessing_call(content, data)  # bytes

    print(type(img))

    embedding_bytes = model_call(img, data)  # list[float]

    print(type(embedding_bytes))

    embeddings = json.loads(embedding_bytes.decode("utf-8"))

    print(type(embeddings))

    embeddings = embeddings["embeddings"]

    print(type(embeddings))

    result = retrieval_store(bow_id, embeddings)

    print(result)

    response = {
        "bow_id": bow_id,
        "embeddings": embeddings,
        "maker": maker,
        "bow_kind": bow_kind,
        "owner": owner,
    }

    return JSONResponse(response)
