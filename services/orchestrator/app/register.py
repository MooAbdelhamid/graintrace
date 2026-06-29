import json
import uuid

from clients.metadata import meta_store
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
    content = await file.read()  # bytes

    data = {"filename": file.filename, "type": file.content_type}

    bow_id = generate_bow_id()  # orchestrator assigns the system ID

    img = preprocessing_call(content, data)  # bytes

    embedding_bytes = model_call(img, data)  # bytes

    embeddings = json.loads(embedding_bytes.decode("utf-8"))  # dict

    embeddings = embeddings["embeddings"]  # list

    result = retrieval_store(bow_id, embeddings)

    print((result))

    metadata = {"bow_id": bow_id, "maker": maker, "bow_kind": bow_kind, "owner": owner}

    metadata_result = meta_store(**metadata)

    print(metadata_result)

    response = {
        "status": "success",
        "bow_id": bow_id,
        "maker": maker,
        "bow_kind": bow_kind,
        "owner": owner,
        "embedding_dimension": len(embeddings),
        "message": f"{bow_id} stored successfully",
    }

    return JSONResponse(response)
