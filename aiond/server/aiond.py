import argparse
import json
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import uvicorn

# Ensure repository root is importable
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from aiond.protocol.request import AnalyzeRequest
from aiond.protocol.response import AnalyzeResponse
from aiond.server.audit_engine import analyze_file
from ledger.merkle_engine import build_merkle_root
from ledger.signer import ensure_keys_present, sign, verify_signature
from proceduralist.hash_engine import compute_sha256

app = FastAPI(title="AION Daemon", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    try:
        result = analyze_file(request.path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:  # pylint: disable=broad-except
        raise HTTPException(status_code=400, detail=str(exc))
    return JSONResponse(content=result)


def _self_test() -> bool:
    # Verify keys
    if not ensure_keys_present():
        return False

    test_payload = json.dumps({"hash": "abc", "merkle_root": "def"}).encode("utf-8")
    signature = sign(test_payload)
    verify_signature(test_payload, signature)

    # Verify Merkle engine
    root = build_merkle_root("abc", ["contradiction"])
    if not isinstance(root, str) or len(root) == 0:
        return False

    # Verify hash engine matches hashlib
    sample_path = REPO_ROOT / "README.md"
    if not sample_path.exists():
        return False
    from hashlib import sha256

    expected = sha256(sample_path.read_bytes()).hexdigest()
    actual = compute_sha256(str(sample_path))
    return expected == actual


def main():
    parser = argparse.ArgumentParser(description="AION Daemon")
    parser.add_argument("--self-test", action="store_true", help="Run self-tests and exit")
    args = parser.parse_args()

    if args.self_test:
        ok = _self_test()
        sys.exit(0 if ok else 1)

    if not _self_test():
        print("Self-test failed; refusing to start daemon", file=sys.stderr)
        sys.exit(1)

    uvicorn.run("aiond.server.aiond:app", host="127.0.0.1", port=7777, reload=False)


if __name__ == "__main__":
    main()
