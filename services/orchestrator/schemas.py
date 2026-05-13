from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class VerifyRequest(BaseModel):
    image_path: str
    top_k: Optional[int] = 5
    threshold: Optional[float] = 0.85


class MatchResult(BaseModel):
    bow_id: str
    score: float


class VerifyResponse(BaseModel):
    decision: str
    matches: List[MatchResult]
    metadata: Optional[Dict[str, Any]] = None
