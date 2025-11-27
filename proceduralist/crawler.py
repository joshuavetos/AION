from pathlib import Path
from typing import Tuple


def extract_text(file_path: str) -> Tuple[str, Path]:
    """
    Read a plaintext file and return its contents and resolved path.
    Only .txt files are supported to keep ingestion deterministic.
    """
    resolved_path = Path(file_path).expanduser().resolve(strict=True)
    if resolved_path.suffix.lower() != ".txt":
        raise ValueError(f"Unsupported file type for ingestion: {resolved_path.suffix}")

    text = resolved_path.read_text(encoding="utf-8")
    return text, resolved_path
