import json
from typing import Dict

from proceduralist.crawler import extract_text
from proceduralist.hash_engine import compute_sha256
from tessrax.governance.kernel import GovernanceKernel
from tessrax.metabolism.contradiction_finder import find_contradictions
from ledger.merkle_engine import build_merkle_root
from ledger.signer import sign


def analyze_file(path: str) -> Dict:
    text, resolved_path = extract_text(path)
    file_hash = compute_sha256(str(resolved_path))
    contradictions = find_contradictions(text)
    sorted_contradictions = sorted(contradictions)

    governance = GovernanceKernel()
    metrics = governance.evaluate(contradictions)

    merkle_root = build_merkle_root(file_hash, contradictions)
    receipt_payload = {
        "hash": file_hash,
        "merkle_root": merkle_root,
        "contradictions": sorted_contradictions,
        "path": str(resolved_path),
    }
    signature = sign(json.dumps(receipt_payload, sort_keys=True).encode("utf-8"))

    return {
        "integrity_score": metrics["integrity_score"],
        "entropy": metrics["entropy"],
        "contradictions": contradictions,
        "receipt": {**receipt_payload, "signature": signature},
    }
