from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ledger.merkle_engine import build_merkle_root
from ledger.signer import ensure_keys, sign, verify_signature
from proceduralist.crawler import extract_text
from proceduralist.hash_engine import compute_sha256
from tessrax.metrics.epistemic_health import calculate_entropy, calculate_integrity
from tessrax.metabolism.contradiction_finder import find_contradictions

app = FastAPI(title="AION Daemon", version="1.0.0")


class AnalyzeRequest(BaseModel):
    path: str


@app.post("/analyze")
def analyze(payload: AnalyzeRequest):
    file_path = Path(payload.path)
    if not file_path.is_file():
        raise HTTPException(status_code=400, detail="Path must point to an existing file")

    try:
        text = extract_text(file_path)
        file_hash = compute_sha256(file_path)
        contradictions = find_contradictions(text)
        entropy = calculate_entropy(contradictions)
        integrity_score = calculate_integrity(contradictions)
        merkle_root = build_merkle_root(file_hash, contradictions)

        receipt_payload = f"{file_hash}:{merkle_root}:{integrity_score}:{entropy}".encode()
        signature = sign(receipt_payload)
    except Exception as exc:  # pragma: no cover - FastAPI handles response
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "integrity_score": integrity_score,
        "entropy": entropy,
        "contradictions": contradictions,
        "receipt": {
            "hash": file_hash,
            "merkle_root": merkle_root,
            "signature": signature,
        },
    }


def _self_test_merkle() -> None:
    sample_root = build_merkle_root("abc", ["one", "two"])
    if not sample_root or len(sample_root) < 10:
        raise RuntimeError("Merkle engine produced an invalid root")


def _self_test_hash_engine() -> None:
    temp_bytes = b"aion-self-test"
    expected = hashlib.sha256(temp_bytes).hexdigest()
    actual = compute_sha256(temp_bytes)
    if actual != expected:
        raise RuntimeError("Hash engine mismatch against hashlib")


def _self_test_signer() -> None:
    ensure_keys()
    payload = b"aion-signer-test"
    signature = sign(payload)
    if not verify_signature(payload, signature):
        raise RuntimeError("Signature verification failed for generated keys")


def run_self_test() -> None:
    _self_test_signer()
    _self_test_merkle()
    _self_test_hash_engine()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AION Daemon")
    parser.add_argument("--self-test", action="store_true", help="Run daemon self-test and exit")
    args = parser.parse_args()

    if args.self_test:
        try:
            run_self_test()
        except Exception as exc:  # pragma: no cover - CLI behavior
            print(f"Self-test failed: {exc}", file=sys.stderr)
            sys.exit(1)
        print("Self-test passed")
        sys.exit(0)

    import uvicorn

    uvicorn.run("aiond.server.aiond:app", host="127.0.0.1", port=7777)
