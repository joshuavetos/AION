<div align="center">

PromptForge

The Epistemic Integrity Engine for Generative AI

<p align="center">
<b>PromptForge (formerly Project Slop Drop)</b> is a forensic prompt engineering environment designed to eliminate hallucination, enforce output schemas, and provide cryptographic assurance for AI interactions.
</p>

Documentation | Architecture | Governance Manifest

</div>

🏛️ Executive Summary

In the era of nondeterministic AI models, the "garbage in, garbage out" paradigm has evolved into "ambiguity in, hallucination out."

PromptForge is not a prompt optimizer; it is a Prompt Governance Engine. It applies the Tessrax Epistemic Integrity Framework to raw user input ("slop"), metabolizing it into rigorous, constraint-hardened instruction sets ("artifacts") that guarantee specific model behaviors.

Unlike standard "rewrite" tools which often introduce new ambiguities, PromptForge uses a deterministic Metabolism Engine to detect and resolve:

Unfalsifiable Instructions (e.g., "Write something creative")

Schema Drift (Missing output format definitions)

Context Leakage (Implicit assumptions not grounded in data)

Logical Contradictions (Conflicting operational constraints)

Every refined prompt is issued with a Cryptographic Integrity Receipt, proving that the input meets the AEP-001 (Auto-Executability Protocol) standard.

🏗️ System Architecture

PromptForge operates on a split-stack architecture designed for maximum privacy (local ingestion) and high-assurance verification.

graph TD
    User[User Input (Raw Slop)] --> Ingest[Ingestion Engine]
    Ingest --> Metabolism[Metabolism Engine]
    Metabolism -->|Detect Smells| ContradictionRecords
    ContradictionRecords --> Governance[Governance Kernel]
    Governance -->|Enforce Iron Laws| RefinedArtifact[Governed Prompt]
    Governance -->|Sign| Ledger[Trust Ledger]
    Ledger --> Receipt[Integrity Receipt]
    RefinedArtifact --> Output[Production Output]


Core Subsystems

Module

Designation

Function

Ingestion Engine

core.ingest

Sanitizes input, strips PII, and identifies Target Model constraints (GPT-4, Claude 3, Llama).

Metabolism Engine

core.metabolism

Detects "Prompt Smells" (ambiguity, subjectivity, open loops) and converts them into structured logic.

Governance Kernel

core.governance

The enforcement layer. Applies Iron Laws (e.g., Output must be JSON, Reasoning must precede Answer).

Trust Ledger

core.ledger

Generates a deterministic SHA-256 hash of the prompt and its integrity score, creating an auditable paper trail.

🛡️ Governance & Compliance

PromptForge is built upon the Tessrax Governance Specifications. All code and outputs adhere to the following strictures:

AEP-001: Auto-Executability Protocol

Definition: A prompt must be executable by an AI model without requiring human intuition to resolve ambiguity.

Enforcement: The kernel rejects any instruction set that lacks explicit output formatting (e.g., JSON, Markdown Table, SQL) or clear termination conditions.

RVC-001: Runtime Verification Clause

Definition: The system must verify that the prompt's constraints are logically consistent before execution.

Enforcement: Contradiction detection algorithms scan for conflicting directives (e.g., "Be concise" vs. "Explain in detail") and force resolution.

EAC-001: Evidence Alignment Clause

Definition: All generative outputs must be grounded in provided context.

Enforcement: The system injects "Anti-Confabulation" guardrails, forcing the model to emit INSUFFICIENT_DATA tokens rather than hallucinating facts.

🚀 Installation & Deployment

PromptForge allows for rapid, deterministic deployment via the bootstrap.py orchestrator.

Prerequisites

Python: 3.11+ (Strict Requirement)

Node.js: 18+ (LTS)

OS: Linux, macOS, or Windows (WSL2 recommended)

Quick Start (The "Bootstrap" Method)

We provide a single-command deployment script that creates the virtual environment, installs dependencies, builds the frontend, and links the local daemon.

# 1. Clone the repository
git clone [https://github.com/your-org/slop-drop.git](https://github.com/your-org/slop-drop.git) promptforge
cd promptforge

# 2. Run the Bootstrap Orchestrator
python scripts/bootstrap.py


Manual Start

If you prefer to run services individually:

Backend Daemon (Python/FastAPI):

cd backend
source venv/bin/activate
python -m server.main
# Server active at [http://127.0.0.1:7777](http://127.0.0.1:7777)


Frontend Interface (Electron/Vue):

cd app
npm run dev
