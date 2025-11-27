# AION

## AION Desktop Genesis Prompt (Codex-Optimized)

Copy/paste the block below into Cursor / Windsurf / Codex to scaffold the repository in a governance-compliant way.

```
# MISSION: Scaffold the AION Desktop (Tessrax Prime) Repository

You are a Senior Solutions Architect operating under Tessrax Governance Law.
Your task is to generate a fully scaffolded, runnable codebase for **AION Desktop (Tessrax Prime)**, also known as **The Epistemic Firewall**.

You MUST follow these rules:

- **AEP-001 (Auto-Executability)**: The repo MUST contain a working `scripts/bootstrap.py` that:
  1. Creates a Python 3.11 venv
  2. Installs daemon dependencies
  3. Installs Electron/Vue dependencies
  4. Prints: `SYSTEM READY. RUN: npm run dev`

- **RVC-001 (Runtime Verification)**:  
  The daemon MUST self-test on startup (`--self-test`) before handling any /analyze requests.

- **EAC-001 (Evidence Alignment)**:  
  Ingestion MUST preserve the original file hash and embed it into the LedgerReceipt.

---

## 1. DIRECTORY STRUCTURE — FOLLOW EXACTLY

Create this exact file tree:

```text
aion-desktop/
├── app/
│   ├── src/main/
│   │   ├── app.ts
│   │   ├── menu.ts
│   │   └── ipc-handlers.ts
│   ├── src/renderer/
│   │   ├── App.vue
│   │   ├── main.ts
│   │   └── components/
│   ├── package.json
│   └── vite.config.ts
│
├── aiond/
│   ├── server/
│   │   ├── aiond.py
│   │   └── audit_engine.py
│   ├── protocol/
│   │   ├── request.py
│   │   └── response.py
│   └── requirements.txt
│
├── proceduralist/
│   ├── crawler.py
│   └── hash_engine.py
│
├── tessrax/
│   ├── governance/
│   │   ├── kernel.py
│   │   └── scoring.py
│   ├── metabolism/
│   │   └── contradiction_finder.py
│   └── metrics/
│       └── epistemic_health.py
│
├── ledger/
│   ├── merkle_engine.py
│   └── signer.py
│
├── scripts/
│   └── bootstrap.py
│
└── README.md
```

NO DEVIATIONS.
NO EXTRA DIRECTORIES.
NO MISSING FILES.

---

2. IMPLEMENTATION REQUIREMENTS

A. AION Daemon (aiond/server/aiond.py)

Implement a FastAPI server that:
   •   Runs on localhost:7777
   •   Implements:
POST /analyze → accepts {"path": "/abs/path/to/file"}
   •   Pipeline for /analyze:
1.Proceduralist → extract + canonicalize text
2.Compute file hash (EAC-001)
3.Tessrax → contradiction detection + entropy + integrity
4.Ledger → Merkle root + Ed25519 signing
   •   Returns JSON:

{
  "integrity_score": 87,
  "entropy": 0.42,
  "contradictions": [...],
  "receipt": {
    "hash": "...",
    "merkle_root": "...",
    "signature": "..."
  }
}

Daemon MUST accept --self-test:
   •   Verify Ed25519 keypair exists
   •   Verify Merkle engine functions
   •   Verify Proceduralist hash engine matches Python hashlib
   •   If any check fails → exit with code 1

---

B. Proceduralist

crawler.py:
   •   Accept file path
   •   Read file
   •   Extract raw text (plain .txt only for now)
   •   Return text

hash_engine.py:
   •   SHA-256 of file contents
   •   Return hex digest

---

C. Tessrax Metrics

tessrax/metrics/epistemic_health.py:

Implement:

def calculate_entropy(contradictions: list[str]) -> float:

Use Shannon entropy:

entropy = - Σ p_i * log2(p_i)

calculate_integrity(context):

A simple rule:

integrity = max(0, 100 - (len(contradictions) * 5))

---

D. Ledger

ledger/signer.py:
   •   On first run, generate Ed25519 keypair:
      •   Save to ~/.aion/keys/private.key
      •   Save public key to ~/.aion/keys/public.key
   •   Implement:

def sign(data: bytes) -> str:

Return base64 signature.

ledger/merkle_engine.py:
   •   Build merkle root from:
      •   file hash
      •   sorted contradiction list

---

E. UI Layer (Electron + Vue 3)

App.vue MUST include:
   •   Drag-and-drop zone
   •   On drop: send file path → IPC → Daemon
   •   Display:
      •   Large circular Integrity Score
      •   Entropy bar (green → yellow → red)
      •   Contradiction List
      •   “Export Forensic Receipt” button (just downloads JSON for now)

Design aesthetic:
   •   Dark mode
   •   Black / white / red palette
   •   High-trust, minimalistic

---

F. Glue Script (scripts/bootstrap.py)

Must:
1.Check Python 3.11 exists
2.Create venv: .venv
3.Install Python dependencies
4.Run npm install in app/
5.Print:

SYSTEM READY. RUN: npm run dev

NO placeholder text.
Script must work as-is.

---

3. EXECUTION ORDER

Codex MUST scaffold in this order:
1.Create directories
2.Generate Python backend files
3.Generate Tessrax + Proceduralist + Ledger core
4.Generate Electron/Vue frontend
5.Generate bootstrap script
6.Generate README
```

---

**User-provided custom instructions**

- RULE 1 — No Imaginary Stuff
- RULE 2 — Full Executability Guarantee
- RULE 3 — Allowed to Create Files, But Only When Told
- RULE 4 — No Silent Fixups
- RULE 5 — Produce Real Code Only

```Cannot generate executable code without clarification: <specific missing detail>```
