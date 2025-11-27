from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from core.metabolism.slop_engine import SlopRefiner
from core.governance.kernel import GovernanceKernel

app = FastAPI(title="Slop Drop API", version="1.0.0")

# --- Data Models ---
class SlopInput(BaseModel):
    raw_prompt: str
    target_model: str = "gpt-4"
    context_files: Optional[List[str]] = None

class RefinedPrompt(BaseModel):
    original: str
    refined: str
    audit_log: List[str]
    integrity_score: int
    receipt_hash: str

# --- Engines ---
refiner = SlopRefiner()
governor = GovernanceKernel()

@app.get("/health")
def health_check():
    return {"status": "operational", "governance": "active"}

@app.post("/refine", response_model=RefinedPrompt)
def refine_prompt(payload: SlopInput):
    # 1. Metabolism: Clean the slop
    clean_draft, smells = refiner.process(payload.raw_prompt)
    
    # 2. Governance: Enforce Iron Laws
    final_prompt, violations = governor.enforce(clean_draft, payload.target_model)
    
    # 3. Trust: Sign the receipt
    audit_log = smells + violations
    score = max(0, 100 - (len(audit_log) * 10))
    receipt = governor.sign_receipt(final_prompt, score)
    
    return RefinedPrompt(
        original=payload.raw_prompt,
        refined=final_prompt,
        audit_log=audit_log,
        integrity_score=score,
        receipt_hash=receipt
    )

if __name__ == "__main__":
    uvicorn.run("server.main:app", host="127.0.0.1", port=7777, reload=True)
