# Pydantic models for the retrieval API
from pydantic import BaseModel, Field


class StoreRequest(BaseModel):
    bow_id: str  # links to metadata in postgres
    embedding: list[float]  # 256-dim vector from model service
    threshold: float | None = None  # if set, check_before_adding runs first


class StoreResponse(BaseModel):
    bow_id: str
    status: str  # "stored" or "duplicate"
    warning: str | None = None  # set if a similar bow was found


class SearchRequest(BaseModel):
    embedding: list[float]  # query embedding to search against
    top_k: int = Field(default=3, ge=1, le=10)


class SearchResult(BaseModel):
    bow_id: str  # use this to fetch metadata from postgres
    score: float = Field(...)


class SearchResponse(BaseModel):
    results: list[SearchResult]
    top_k: int


class SearchByIdResponse(BaseModel):
    bow_id: str
    embedding: list[float]  # full embedding vector stored in qdrant


class DeleteAllResponse(BaseModel):
    status: str  # "deleted_all"
