from __future__ import annotations

import hashlib
from typing import List


def _hash_pair(left: str, right: str) -> str:
    return hashlib.sha256((left + right).encode()).hexdigest()


def build_merkle_root(file_hash: str, contradictions: List[str]) -> str:
    nodes: List[str] = [file_hash] + sorted(contradictions)
    if not nodes:
        raise ValueError("Cannot build merkle root without data")

    while len(nodes) > 1:
        next_level: List[str] = []
        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i + 1] if i + 1 < len(nodes) else nodes[i]
            next_level.append(_hash_pair(left, right))
        nodes = next_level
    return nodes[0]
