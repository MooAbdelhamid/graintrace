# Pydantic models for the retrieval API
from pydantic import BaseModel, Field


class StoreRequest(BaseModel):
    bow_id: str  # links to metadata in postgres
    embedding: list[float]  # 256-dim vector from model service


class StoreResponse(BaseModel):
    bow_id: str
    status: str  # "stored"


class SearchRequest(BaseModel):
    embedding: list[float]  # query embedding to search against
    top_k: int = Field(default=3, ge=1, le=10)


class SearchResult(BaseModel):
    bow_id: str  # use this to fetch metadata from postgres
    score: float = Field(..., ge=0.0, le=1.0)  # cosine similarity 0..1


class SearchResponse(BaseModel):
    results: list[SearchResult]
    top_k: int
