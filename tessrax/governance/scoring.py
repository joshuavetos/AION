from __future__ import annotations

from dataclasses import dataclass
from tessrax.metrics.epistemic_health import calculate_entropy, calculate_integrity
from tessrax.metabolism.contradiction_finder import find_contradictions


@dataclass
class GovernanceScore:
    contradictions: list[str]
    entropy: float
    integrity: int


def score_document(text: str) -> GovernanceScore:
    contradictions = find_contradictions(text)
    entropy = calculate_entropy(contradictions)
    integrity = calculate_integrity(contradictions)
    return GovernanceScore(contradictions=contradictions, entropy=entropy, integrity=integrity)
