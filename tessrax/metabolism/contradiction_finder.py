from __future__ import annotations

import re
from typing import List


_CONTRADICTION_PATTERNS = [
    (re.compile(r"\bdo not\b.*\bbut also\b", re.IGNORECASE), "Conflicting directive: negative + positive instruction"),
    (re.compile(r"\bconcise\b.*\bdetailed\b", re.IGNORECASE), "Conflicting verbosity requirements"),
    (re.compile(r"\bfacts\b.*\bmake them up\b", re.IGNORECASE), "Fact-based request conflicts with creative fabrication"),
]


def find_contradictions(text: str) -> List[str]:
    findings: List[str] = []
    for pattern, description in _CONTRADICTION_PATTERNS:
        if pattern.search(text):
            findings.append(description)
    return findings
