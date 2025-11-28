from __future__ import annotations

import math
from collections import Counter
from typing import List


def calculate_entropy(contradictions: List[str]) -> float:
    if not contradictions:
        return 0.0
    counts = Counter(contradictions)
    total = sum(counts.values())
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    return round(entropy, 4)


def calculate_integrity(contradictions: List[str]) -> int:
    return max(0, 100 - (len(contradictions) * 5))
