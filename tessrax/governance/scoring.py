from typing import List

from tessrax.metrics.epistemic_health import calculate_entropy, calculate_integrity


def score_document(contradictions: List[str]) -> dict:
    return {
        "entropy": calculate_entropy(contradictions),
        "integrity_score": calculate_integrity(contradictions),
    }
