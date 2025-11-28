from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Union


def _digest_bytes(data: bytes) -> str:
    hasher = hashlib.sha256()
    hasher.update(data)
    return hasher.hexdigest()


def compute_sha256(source: Union[str, Path, bytes]) -> str:
    if isinstance(source, (str, Path)):
        path = Path(source)
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {path}")
        return _digest_bytes(path.read_bytes())
    if isinstance(source, bytes):
        return _digest_bytes(source)
    raise TypeError("Unsupported input type for compute_sha256")
