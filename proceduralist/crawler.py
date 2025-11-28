from pathlib import Path


def extract_text(path: Path) -> str:
    path = Path(path)
    if path.suffix.lower() != ".txt":
        raise ValueError("Only .txt files are supported for ingestion")
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    return path.read_text(encoding="utf-8")
