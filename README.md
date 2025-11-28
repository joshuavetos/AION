# AION Desktop (Tessrax Prime)

AION Desktop is the governance-compliant "Epistemic Firewall" that pairs a FastAPI daemon with an Electron + Vue 3 interface. The system ingests plaintext evidence, computes integrity signals, and produces a signed, Merkle-anchored receipt for every analysis.

## Repository Layout

```
app/
  src/main/            # Electron main process
  src/renderer/        # Vue 3 renderer
  package.json
  vite.config.ts

aiond/
  server/              # FastAPI daemon and audit engine
  protocol/            # Request/response models
  requirements.txt

proceduralist/         # File ingestion + hashing

tessrax/               # Governance metrics and contradiction detection

ledger/                # Merkle root builder + Ed25519 signer

scripts/bootstrap.py   # Environment bootstrapper
```

## Getting Started

1. **Bootstrap the environment** (creates `.venv`, installs Python + frontend deps; enforces Python 3.11 and Node 18+):

   ```bash
   python3 scripts/bootstrap.py
   ```

   On success the script prints `SYSTEM READY. RUN: npm run dev`.

2. **Run the daemon** (self-test enforced at startup):

   ```bash
   .venv/bin/python aiond/server/aiond.py
   ```

   - `--self-test` exits after running the runtime verification checks.
   - The API listens on `http://127.0.0.1:7777` with `POST /analyze` accepting `{ "path": "/abs/path/to/file.txt" }`.

3. **Run the desktop app** (from the `app/` directory):

   ```bash
   npm run dev
   ```

   The renderer dev server runs on port 5173 and the Electron shell attaches automatically.

## Daemon Pipeline

1. **Proceduralist** — reads `.txt` files only and computes a SHA-256 hash (EAC-001). Non-`.txt` files are rejected in the renderer before invoking the daemon.
2. **Tessrax** — performs contradiction detection and calculates entropy + integrity scores.
3. **Ledger** — builds a Merkle root from the file hash and contradictions, then signs the receipt with an Ed25519 key pair stored under `~/.aion/keys`.

Example response:

```json
{
  "integrity_score": 87,
  "entropy": 0.42,
  "contradictions": ["..."],
  "receipt": {
    "hash": "...",
    "merkle_root": "...",
    "signature": "..."
  }
}
```

## Frontend Highlights

- Drag-and-drop zone that sends file paths over IPC to the daemon
- Large circular integrity score, entropy bar, and contradiction list
- "Export Forensic Receipt" button to download the JSON response
- Dark, black/white/red theme tuned for a high-trust aesthetic

## Governance Guarantees

- **AEP-001**: `scripts/bootstrap.py` provisions both Python (3.11) and Electron/Vue dependencies and prints the required readiness string.
- **RVC-001**: The daemon runs a self-test on startup (or via `--self-test`) validating the signer, Merkle engine, and hash pipeline before serving requests.
- **EAC-001**: The original file hash is preserved in the signed ledger receipt for every analysis.
