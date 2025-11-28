from pydantic import BaseModel
from typing import List


class Receipt(BaseModel):
    hash: str
    merkle_root: str
    signature: str


class AnalyzeResponse(BaseModel):
    integrity_score: int
    entropy: float
    contradictions: List[str]
    receipt: Receipt
