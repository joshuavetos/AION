import hashlib
from typing import List


def _hash_leaf(value: str) -> bytes:
    return hashlib.sha256(value.encode("utf-8")).digest()


def _hash_pair(left: bytes, right: bytes) -> bytes:
    return hashlib.sha256(left + right).digest()


def build_merkle_root(file_hash: str, contradictions: List[str]) -> str:
    leaves: List[bytes] = [_hash_leaf(file_hash)]
    for entry in sorted(contradictions):
        leaves.append(_hash_leaf(entry))

    if not leaves:
        return file_hash

    current_level = leaves
    while len(current_level) > 1:
        next_level: List[bytes] = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1] if i + 1 < len(current_level) else current_level[i]
            next_level.append(_hash_pair(left, right))
        current_level = next_level

    return current_level[0].hex()
