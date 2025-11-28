from typing import Dict, List

from tessrax.metrics.epistemic_health import calculate_entropy, calculate_integrity


class GovernanceKernel:
    """
    Core governance evaluator responsible for aggregating epistemic metrics.
    """

    def evaluate(self, contradictions: List[str]) -> Dict[str, float | int]:
        entropy = calculate_entropy(contradictions)
        integrity = calculate_integrity(contradictions)
        return {
            "entropy": entropy,
            "integrity_score": integrity,
        }
