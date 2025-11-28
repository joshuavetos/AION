# AION Desktop (Tessrax Prime)

AION Desktop is the Epistemic Firewall for local prompt forensics. The stack includes a FastAPI daemon, Tessrax governance engines, a ledgered receipt pipeline, and an Electron/Vue interface for drag-and-drop analysis.

## Directory layout

- `aiond/` – FastAPI daemon and protocol contracts
- `proceduralist/` – File ingestion and hashing utilities
- `tessrax/` – Governance, metabolism, and metrics modules
- `ledger/` – Merkle tree and Ed25519 signing
- `app/` – Electron + Vue frontend
- `scripts/` – Bootstrap automation

## Getting started

1. **Bootstrap**
   ```bash
   python scripts/bootstrap.py
   ```
2. **Run the daemon**
   ```bash
   source .venv/bin/activate
   python -m aiond.server.aiond --self-test
   python -m aiond.server.aiond
   ```
3. **Start the desktop app**
   ```bash
   cd app
   npm run dev
   ```

Drop a `.txt` file onto the UI to send it to the daemon. The response includes integrity score, entropy, contradictions, and a signed forensic receipt with the original file hash, Merkle root, and Ed25519 signature.
