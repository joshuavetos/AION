from __future__ import annotations

from tessrax.governance.scoring import GovernanceScore, score_document


def evaluate(text: str) -> GovernanceScore:
    """Run governance scoring over provided text."""
    return score_document(text)
