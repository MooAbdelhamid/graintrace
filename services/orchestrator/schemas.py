from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class MatchResult(BaseModel):
    bow_id: str
    score: float


class VerifyResponse(BaseModel):
    decision: str
    matches: List[MatchResult]
    metadata: Optional[Dict[str, Any]] = None
