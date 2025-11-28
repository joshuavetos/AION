from pydantic import BaseModel


class Receipt(BaseModel):
    hash: str
    merkle_root: str
    signature: str


class AnalyzeResponse(BaseModel):
    integrity_score: int
    entropy: float
    contradictions: list[str]
    receipt: Receipt
