import hashlib
from pathlib import Path


def compute_sha256(file_path: str) -> str:
    """
    Compute the SHA-256 hash of a file's contents and return the hex digest.
    """
    resolved_path = Path(file_path).expanduser().resolve(strict=True)
    digest = hashlib.sha256()
    with resolved_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()
