# FastAPI router for the retrieval service
# POST /store  saves embedding to qdrant
# POST /search finds closest matches by cosine similarity
from app.models import (
    SearchRequest,
    SearchResponse,
    SearchResult,
    StoreRequest,
    StoreResponse,
)
from db.qdrant_manager import QdrantManager
from fastapi import APIRouter

router = APIRouter()

qdrant_manager = QdrantManager()


@router.post("/store", response_model=StoreResponse)
def store(request: StoreRequest):
    # input:  bow_id + embedding vector
    # output: confirmation with bow_id and status
    qdrant_manager.store(request.bow_id, request.embedding)
    return StoreResponse(bow_id=request.bow_id, status="stored")


@router.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):
    # input:  query embedding + top_k
    # output: list of {bow_id, score} sorted by similarity
    # bow_id is the link back to postgres metadata
    results = qdrant_manager.search(request.embedding, request.top_k)
    return SearchResponse(
        results=[SearchResult(**r) for r in results],
        top_k=request.top_k,
    )


@router.delete("/delete/{bow_id}")
def delete(bow_id: str):
    qdrant_manager.delete(bow_id)
    return {"bow_id": bow_id, "status": "deleted"}
