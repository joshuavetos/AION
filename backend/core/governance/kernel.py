import hashlib
import time

class GovernanceKernel:
    """
    The Governance Kernel: Enforces 'Iron Laws' and issues cryptographic receipts.
    """
    
    def enforce(self, draft_prompt: str, model: str) -> tuple[str, list[str]]:
        violations = []
        final_prompt = draft_prompt

        # Iron Law 1: Output Format Mandatory
        if "JSON" not in draft_prompt and "Markdown" not in draft_prompt:
            final_prompt += "- Output Format: STRICT JSON (valid RFC 8259).\n"
            violations.append("Iron Law 1 Violation: No output format specified. Enforcing JSON.")

        # Iron Law 2: Chain of Thought
        if "step-by-step" not in draft_prompt.lower():
            final_prompt += "- Reasoning: Think step-by-step in <scratchpad> tags before answering.\n"
            violations.append("Iron Law 2 Violation: No reasoning step. Enforcing CoT.")

        # Iron Law 3: Anti-Hallucination (Evidence Alignment)
        final_prompt += "- Grounding: Answer ONLY using provided context. If unsure, state 'Insufficient Data'.\n"
        
        return final_prompt, violations

    def sign_receipt(self, content: str, score: int) -> str:
        """Generates a deterministic hash (Simulated Ed25519 for MVP)"""
        payload = f"{content}{score}{time.time()}"
        return hashlib.sha256(payload.encode()).hexdigest()[:16]
