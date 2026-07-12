# FastAPI router for the retrieval service
# POST /store       saves embedding to qdrant, optional duplicate check via threshold
# POST /search      finds closest matches by cosine similarity
# GET  /search/{id} fetches a single point by bow_id
# DELETE /delete/{id}  deletes a single bow
# DELETE /delete-all   deletes all embeddings
from app.models import (
    DeleteAllResponse,
    SearchByIdResponse,
    SearchRequest,
    SearchResponse,
    SearchResult,
    StoreRequest,
    StoreResponse,
)
from db.qdrant_manager import QdrantManager
from fastapi import APIRouter, HTTPException

router = APIRouter()

qdrant_manager = QdrantManager()


@router.post("/store", response_model=StoreResponse)
def store(request: StoreRequest):
    # input:  bow_id + embedding vector, optional threshold for duplicate check
    # output: confirmation with bow_id and status, warning if duplicate found
    if request.threshold is not None:
        match = qdrant_manager.check_before_adding(request.embedding, request.threshold)
        if match:
            # similar bow found, return warning without storing
            return StoreResponse(
                bow_id=request.bow_id,
                status="duplicate",
                warning=f"Similar bow already exists: {match['bow_id']} "
                f"(score: {match['score']:.4f})",
            )

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


@router.get("/search/{bow_id}", response_model=SearchByIdResponse)
def search_by_id(bow_id: str):
    # input:  bow_id string
    # output: bow_id + full embedding vector, 404 if not found
    result = qdrant_manager.search_by_id(bow_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"{bow_id} not found")
    return SearchByIdResponse(**result)


@router.delete("/delete/{bow_id}")
def delete(bow_id: str):
    print("in delete")
    qdrant_manager.delete(bow_id)
    return {"bow_id": bow_id, "status": "deleted"}


@router.delete("/delete-all", response_model=DeleteAllResponse)
def delete_all():
    # deletes all embeddings by dropping and recreating the collection
    qdrant_manager.delete_all()
    return DeleteAllResponse(status="deleted_all")
