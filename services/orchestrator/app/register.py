import json
import uuid

from clients.metadata import meta_store
from clients.model import model_call
from clients.preprocessing import preprocessing_call
from clients.retrieval import retrieval_store
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from models.bow import Bow

router = APIRouter(prefix="/register", tags=["register"])


def generate_bow_id() -> str:
    # orchestrator assigns bow_id in format BOW-XXXXXX
    return f"BOW-{uuid.uuid4().hex[:6].upper()}"


@router.post("/")
async def register(file: UploadFile = File(...), bow: Bow = Depends(Bow.as_form)):
    # input:  JPEG image + bow passport fields as form fields
    # output: EnrollResponse with bow_id, embedding_dim, status, passport

    print("Request IN")

    content = await file.read()  # bytes

    # move into preprocessing call
    data = {"filename": file.filename, "type": file.content_type}

    print("ID Generated")

    bow_id = generate_bow_id()  # orchestrator assigns the system ID

    print("Calling Preprocessing")

    # add the if condition
    img = preprocessing_call(content, data)  # bytes

    if img == b"null":
        return {"status": "fail", "message": "invalid image provided"}

    print("Calling Model")

    embedding_bytes = model_call(img, data)  # bytes

    embeddings = json.loads(embedding_bytes.decode("utf-8"))  # dict

    print(embeddings)

    embeddings = embeddings["embeddings"]  # list

    print("Calling Retrieval")

    result = retrieval_store(bow_id, embeddings)

    print((result))

    return {"result": result}
    # adjust all of this
    metadata = {"bow_id": bow_id, "maker": maker, "bow_kind": bow_kind, "owner": owner}

    print("Calling Metadata")

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
