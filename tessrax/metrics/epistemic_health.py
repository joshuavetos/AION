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
        probability = count / total
        entropy -= probability * math.log2(probability)
    return entropy


def calculate_integrity(contradictions: List[str]) -> int:
    integrity = max(0, 100 - (len(contradictions) * 5))
    return integrity
